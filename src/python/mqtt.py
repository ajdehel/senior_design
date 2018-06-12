import json
import paho.mqtt.client as mqtt
import time

class Client:

    def __init__(self, ip_addr=None):
        self._client = mqtt.Client()
        self._client.on_message = on_message
        self._client.on_connect = on_connect
        self._client.on_subscribe = on_subscribe
        self.ip_addr = ip_addr
        self.port = 1883

    def __enter__(self):
        self.connect(self.ip_addr)
        return self

    def __exit__(self, type, value, traceback):
        self.disconnect()

    def connect(self, ip_addr=None):
        print(f"connecting to {ip_addr}...")
        if self.ip_addr is None:
            self.ip_addr = ip_addr
        self._client.connect(self.ip_addr, port=self.port)

    def subscribe(self, topic):
        print(f"subscribing to {topic}...")
        self._client.subscribe(topic)

    def disconnect(self):
        self._client.disconnect()

    def check_for_data(self):
        self._client.loop(timeout=5.0)

def on_subscribe(client, userdata, mid, granted_qos):
    print(mid)

def on_connect(client, userdata, flags, rc):
    print(rc)

def on_message(client, userdata, message):
    print(json.loads(message.payload, encoding="utf-8"))
