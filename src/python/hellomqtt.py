import mqtt
import time

AWS_IP_ADDR = "18.217.132.144"

def main():
    with mqtt.Client(ip_addr=AWS_IP_ADDR, client_id="pyclient") as client:
        client.subscribe("helloworld")
        while True:
            client.check_for_data()

if __name__ == "__main__":
    main()

