import collections
import datetime
import json
import logging
import paho.mqtt.client as mqtt
import time
from __init__ import Message


LOGGER = logging.getLogger("PLUMBINTEL")

class Client(mqtt.Client):

    def __init__(self, ip_addr=None, port=None, **kwargs):
        super().__init__(**kwargs)
        self.ip_addr = ip_addr
        self.port = port
        self.database = None
        self._thread_running = False
        self.message_queue = collections.deque()
        self.on_connect = on_connect
        self.on_subscribe = on_subscribe
        self.on_message = on_message

    def connect(self, ip_addr=None, port=1883, **kwargs):
        self.ip_addr = ip_addr if self.ip_addr is None else self.ip_addr
        self.port = port if self.port is None else self.port
        if self.ip_addr is None or self.port is None:
            raise Exception()
        else:
            super().connect(self.ip_addr, self.port, **kwargs)
            LOGGER.info(f"Connected to {self.ip_addr}:{self.port}")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, e_type, e_value, e_traceback):
        if e_type:
            LOGGER.error(str(e_type))
        if self._thread_running:
            self.loop_stop()
            self._thread_running = False
        self.disconnect()

    def check_for_data(self, timeout=5.0):
        self.loop(timeout=timeout)

    def start_thread(self):
        self.loop_start()
        self._thread_running = True

    def handle_message(self, payload):
        timestamp = datetime.datetime.now()
        self.message_queue.append(Message(payload, timestamp))

def on_connect(client, userdata, flags, rc):
    LOGGER.info(f"client connected to {client.ip_addr}")

def on_subscribe(client, userdata, mid, granted_qos):
    LOGGER.info("client subscribed")

def on_message(client, userdata, message):
    LOGGER.debug(f"Received message from broker")
    client.handle_message(message.payload)

