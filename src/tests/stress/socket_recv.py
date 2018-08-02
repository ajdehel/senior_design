import time
import plumbintel
from plumbintel import udp

config = plumbintel.configure()

queue = None

with udp.Listener(ip_addr=config["Listener"]["host"],
                  port=config["Listener"]["port"]) as listener:
    listener.start_thread()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    queue_size = len(list(listener.message_queue))
print(f"Messages received {queue_size}")

