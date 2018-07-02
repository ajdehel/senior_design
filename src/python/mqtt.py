import json
import logging
import paho.mqtt.client as mqtt
import time

LOGGER = logging.getLogger(__name__)
LOG_FORMAT = "{asctime} -- {levelname} -- {filename} -- {message}"
FORMATTER = logging.Formatter(fmt=LOG_FORMAT, style="{")
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(CONSOLE_HANDLER)
LOGGER.setLevel(logging.DEBUG)

class Client(mqtt.Client):

    def __init__(self, ip_addr=None, port=None, **kwargs):
        super().__init__(**kwargs)
        self.ip_addr = ip_addr
        self.port = port
        self.on_connect = on_connect
        self.on_subscribe = on_subscribe
        self.on_message = on_message

    def connect(self, ip_addr=None, port=1883, **kwargs):
        self.ip_addr = ip_addr if self.ip_addr is None else self.ip_addr
        self.port = port if self.port is None else self.port
        LOGGER.debug(f"connecting to {self.ip_addr}:{self.port}")
        if self.ip_addr is None or self.port is None:
            raise Exception()
        else:
            super().connect(self.ip_addr, self.port, **kwargs)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, e_type, e_value, e_traceback):
        if e_type:
            LOGGER.error(str(e_type))
        self.disconnect()

    def check_for_data(self):
        self.loop(timeout=5.0)

def on_connect(client, userdata, flags, rc):
    LOGGER.info(f"client connected to {client.ip_addr}")

def on_subscribe(client, userdata, mid, granted_qos):
    LOGGER.info("client subscribed")

def on_message(client, userdata, message):
    LOGGER.info("message received")
    payload = json.loads(message.payload, encoding="utf-8")
    LOGGER.debug(f"payload: {payload}")

