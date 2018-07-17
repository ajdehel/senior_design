import socket
import time
import udp

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = "Hello, World!"

send_sock = socket.socket(socket.AF_INET, # Internet
                          socket.SOCK_DGRAM) # UDP

with udp.Listener(ip_addr=UDP_IP, port=UDP_PORT) as listener:
    offset=0
    while True:
        for i in range(0,10):
            message = f"{MESSAGE}:{i+offset}"
            send_sock.sendto(bytes(message, encoding="UTF-8"), (UDP_IP, UDP_PORT))
        listener.check_for_data()
        for each in list(listener.message_queue):
            print(each)
        offset+=10
        time.sleep(1)

