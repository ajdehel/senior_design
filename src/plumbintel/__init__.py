"""
Program to coordinate communication between MQTT broker and SQL
    Server for PlumbInteligent System.
"""
import logging
import json
import mqtt
import sql
import time

#Logging set-up
LOGGER = logging.getLogger("PLUMBINTEL")
LOG_FORMAT = "{asctime} - {name} - {filename}:{lineno} - {levelname} - {message}"
FORMATTER = logging.Formatter(fmt=LOG_FORMAT, style="{")
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(CONSOLE_HANDLER)
LOGGER.setLevel(logging.DEBUG)

#Constants for establishing connections
CONF_PATH = "/etc/plumbintel.conf"

def parse_device_packet(packet):
    """Parse packets, convert voltage to correct form and return list for SQL DB.
        Plumbintel packets are expected to be in the following form:
        - "tuple(bytestring, datetime.datetime())"
          - bytestring: ["<device_id>", <voltage_reading>]
        Output:
        - list[str(device_id), int(evaluated_reading), str(timestamp)]
    """
    try:
        sql_payload = json.loads(message[0], encoding="utf-8")
        LOGGER.debug(f"payload: {payload}")
        return sql_payload
    except json.decoder.JSONDecodeError as error:
        LOGGER.error(f"received improperly formatted payload {str(message.payload)}")

def configure():
    """Configures all the necessary variables for operation.
        ***MUST BE RUN FIRST***
    """
    conf = None
    try:
        with open(CONF_PATH, mode='r') as conf_file:
            conf = json.load(conf_file)
            LOGGER.info("Successfully read in conf_file")
            return conf
    except json.decoder.JSONDecodeError as e:
        LOGGER.critical(f"Could not parse config at {CONF_PATH}.")
    except FileNotFoundError as e:
        LOGGER.critical(f"Could not find config as {CONF_PATH}.")
    except PermissionError as e:
        LOGGER.critical(f"Could not open {CONF_PATH}. Escalate Permissions.")

def main(config):
    with sql.Database(**config["SQL"], timeout=30) as db:
        with udp.Listener(ip_addr=MQTT_BROKER_HOST,
                          port=MQTT_BROKER_PORT) as listener:
            while True:
                listener.check_for_data()

if __name__ == "__main__":
    config = configure()
    main(config)

