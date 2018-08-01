import logging
import json
import time
import pypyodbc
import threading
from . import sql
from . import udp
from . import mqtt
from . import CONF_PATH

LOGGER = logging.getLogger("PLUMBINTEL")

INSERTIONS = 0

def parse_device_packet(packet):
    """Parse packets, convert voltage to correct form and return list for SQL DB.
        Plumbintel packets are expected to be in the following form:
        - "tuple(bytestring, datetime.datetime())"
          - bytestring: ["<device_id>", <voltage_reading>]
        Output:
        - list[str(device_id), int(evaluated_reading), str(timestamp)]
    """
    try:
        sql_payload = json.loads(packet.contents, encoding="utf-8")
        timestamp = packet.timestamp.strftime(f"%Y-%m-%d %H:%M:%S.%f")
        sql_payload.append(timestamp)
        return sql_payload
    except json.decoder.JSONDecodeError as error:
        LOGGER.error(f"received improperly formatted packet {str(packet.contents)}")

def configure():
    """Configures all the necessary variables for operation.
        ***MUST BE RUN FIRST***
    """
    conf = None
    conf_path = CONF_PATH
    try:
        with open(conf_path, mode='r') as conf_file:
            conf = json.load(conf_file)
            LOGGER.info("Successfully read in conf_file")
            return conf
    except json.decoder.JSONDecodeError as e:
        LOGGER.critical(f"Could not parse config at {conf_path}.")
    except FileNotFoundError as e:
        LOGGER.critical(f"Could not find config as {conf_path}.")
    except PermissionError as e:
        LOGGER.critical(f"Could not open {conf_path}. Escalate Permissions.")
    raise Exception

def insert_into_database(db, db_table, queue):
    global INSERTIONS
    insertions = 0
    try:
        while True:
            packet = queue.popleft()
            sql_payload = parse_device_packet(packet)
            if sql_payload is not None:
                db.insert(db_table, sql_payload)
                insertions += 1
    except IndexError as e:
        LOGGER.info(f"Inserted {insertions} entries into the Database")
    except pypyodbc.DatabaseError as e:
        LOGGER.error("Could not insert entry into db")
    INSERTIONS += insertions

def main(config):
    with sql.Database(**config["SQL"]["Connection"], timeout=30) as db:
        with udp.Listener(ip_addr=config["Listener"]["host"],
                          port=config["Listener"]["port"]) as listener:
            listener.start_thread()
            while True:
                time.sleep(10.0)
                insert_into_database(db, config["SQL"]["table"], listener.message_queue)

def main2(config):
    with sql.Database(**config["SQL"]["Connection"], timeout=30) as db:
        with mqtt.Client(ip_addr=config["MQTT"]["host"],
                          port=config["MQTT"]["port"]) as client:
            client.subscribe(config["MQTT"]["topic"])
            client.start_thread()
            while True:
                time.sleep(10.0)
                insert_into_database(db, config["SQL"]["table"], client.message_queue)

if __name__ == "__main__":
    config = configure()
    try:
        main(config)
    except KeyboardInterrupt:
        print(INSERTIONS)

