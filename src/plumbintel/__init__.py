"""
Program to coordinate communication between MQTT broker and SQL
    Server for PlumbInteligent System.
"""
import logging
import collections
import json

Message = collections.namedtuple("Message", ["contents", "timestamp"])

#Logging set-up
LOGGER = logging.getLogger("PLUMBINTEL")
LOG_FORMAT = "{asctime} - {name} - {module:>8}:{lineno:>3} - {levelname:^8} - {message}"
FORMATTER = logging.Formatter(fmt=LOG_FORMAT, style="{")
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(CONSOLE_HANDLER)
LOGGER.setLevel(logging.INFO)

#Constants for establishing connections
CONF_PATH = "/etc/plumbintel.conf"

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
    except Exception as e:
        LOGGER.error(e)
        LOGGER.error("Could not insert entry into db")


