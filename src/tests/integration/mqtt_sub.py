import time
import plumbintel
from plumbintel import mqtt

config = plumbintel.configure()

queue_size = 0
with mqtt.Client(ip_addr=config["MQTT"]["host"],
                  port=config["MQTT"]["port"]) as client:
    client.subscribe("TEST")
    client.start_thread()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    queue_size = len(list(client.message_queue))
print(f"Received {queue_size} messages.")

