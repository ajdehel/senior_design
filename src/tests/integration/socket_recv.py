import time
import plumbintel
from plumbintel import udp

config = plumbintel.configure()

queue = None
with udp.Listener(ip_addr=config["Listener"]["host"],
                  port=config["Listener"]["port"]) as listener:
    listener.start_thread()
    while True:
        time.sleep(1)
    queue = listener.message_queue
print(f"Messages received {len(queue)}")

