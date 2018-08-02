import logging
import json
import time
import pypyodbc
import threading
from . import sql
from . import udp
from . import mqtt
from . import CONF_PATH, configure, insert_into_database

LOGGER = logging.getLogger("PLUMBINTEL")
def socket_interface(config):
    with sql.Database(**config["SQL"]["Connection"], timeout=30) as db:
        with udp.Listener(ip_addr=config["Listener"]["host"],
                          port=config["Listener"]["port"]) as listener:
            listener.start_thread()
            while True:
                time.sleep(10.0)
                insert_into_database(db, config["SQL"]["table"], listener.message_queue)

def mqtt_interface(config):
    with sql.Database(**config["SQL"]["Connection"], timeout=30) as db:
        with mqtt.Client(ip_addr=config["MQTT"]["host"],
                          port=config["MQTT"]["port"]) as client:
            client.subscribe(config["MQTT"]["topic"])
            client.start_thread()
            while True:
                time.sleep(10.0)
                insert_into_database(db, config["SQL"]["table"], client.message_queue)

def main():
    config = configure()
    mqtt_interface(config)

if __name__ == "__main__":
    main()

