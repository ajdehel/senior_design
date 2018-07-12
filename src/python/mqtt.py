import datetime
import json
import logging
import paho.mqtt.client as mqtt
import time

LOGGER = logging.getLogger("PLUMBINTEL")

MAX_KEEP_ALIVE = 2**16 - 1

class Client(mqtt.Client):

    def __init__(self, ip_addr=None, port=None, keep_alive=60, **kwargs):
        super().__init__(**kwargs)
        self.ip_addr = ip_addr
        self.port = port
        self.database = None
        self.keep_alive = keep_alive
        self.on_connect = on_connect
        self.on_subscribe = on_subscribe
        self.on_message = on_message

    def connect(self, ip_addr=None, port=1883, **kwargs):
        self.ip_addr = ip_addr if self.ip_addr is None else self.ip_addr
        self.port = port if self.port is None else self.port
        LOGGER.debug(f"connecting to {self.ip_addr}:{self.port}")
        kwargs["keepalive"] = self.keep_alive
        if self.ip_addr is None or self.port is None:
            raise Exception()
        else:
            super().connect(self.ip_addr, self.port, **kwargs)

    def accept_database(self, database, table, ):
        if database.connected:
            self.database = database
            self.db_target_table = table

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, e_type, e_value, e_traceback):
        if e_type:
            LOGGER.error(str(e_type))
        self.disconnect()

    def check_for_data(self):
        self.loop(timeout=5.0)

    def handle_message(self, payload):
        if self.database:
            if len(payload) is 3:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                payload = payload[0:2] + [timestamp,] + payload[2:]
            self.database.insert(self.db_target_table, payload)

def on_connect(client, userdata, flags, rc):
    LOGGER.info(f"client connected to {client.ip_addr}")

def on_subscribe(client, userdata, mid, granted_qos):
    LOGGER.info("client subscribed")

def on_message(client, userdata, message):
    LOGGER.info("message received")
    try:
        payload = json.loads(message.payload, encoding="utf-8")
        LOGGER.debug(f"payload: {payload}")
        client.handle_message(payload)
    except json.decoder.JSONDecodeError as error:
        LOGGER.error(f"received improperly formatted payload {str(message.payload)}")

