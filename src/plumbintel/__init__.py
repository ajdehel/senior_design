"""
Program to coordinate communication between MQTT broker and SQL
    Server for PlumbInteligent System.
"""
import logging
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

