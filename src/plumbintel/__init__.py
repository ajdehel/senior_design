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
##MQTT Constants
MQTT_BROKER_HOST = "18.217.132.144"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = "Devices"
##SQL Constants
SQL_SERVER_HOST = "test-mssql.cfblwhszdeig.us-east-2.rds.amazonaws.com"
SQL_SERVER_PORT = "1433"
SQL_DRIVER   = "ODBC Driver 17 for SQL Server"
SQL_DATABASE = "PlumbIntel"
SQL_USERNAME = "testsql"
SQL_PASSWORD = "Testpassword"
SQL_TABLE    = "Devices"

SQL_CONFIG = {"driver": SQL_DRIVER,
              "server": SQL_SERVER_HOST,
              "port": SQL_SERVER_PORT,
              "database": SQL_DATABASE,
              "username": SQL_USERNAME,
              "password": SQL_PASSWORD,
             }
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



def main():
    with sql.Database(**SQL_CONFIG, timeout=30) as db:
        with mqtt.Client(ip_addr=MQTT_BROKER_HOST,
                         port=MQTT_BROKER_PORT,
                         client_id="PLUMBINTEL") as client:
            client.subscribe(MQTT_TOPIC)
            client.accept_database(db, SQL_TABLE)
            while True:
                client.check_for_data()

if __name__ == "__main__":
    main()

