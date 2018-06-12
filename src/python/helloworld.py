import mqtt
import time

AWS_IP_ADDR = "18.217.39.20"

def connect_demo(mqtt_client):
    mqtt_client.connect(AWS_IP_ADDR)

def subscribe_demo(mqtt_client):
    mqtt_client.subscribe("helloworld")

def main():
    client = mqtt.Client()
    client.connect(AWS_IP_ADDR)
    client.subscribe("helloworld")
    try:
        while True:
            client.check_for_data()
    except KeyboardInterrupt:
        client.disconnect

def conman():
    with mqtt.Client(AWS_IP_ADDR) as client:
        client.subscribe("helloworld")
        while True:
            client.check_for_data()

if __name__ == "__main__":
    conman()




