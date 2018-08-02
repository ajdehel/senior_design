import socket
import time

UDP_IP = "18.217.132.144"
UDP_PORT = 10000

send_sock = socket.socket(socket.AF_INET, # Internet
                          socket.SOCK_DGRAM) # UDP

packets_sent = 0
for i in range(0,100000):
    message = f"""["VTEST", {packets_sent}]"""
    send_sock.sendto(bytes(message, encoding="UTF-8"), (UDP_IP, UDP_PORT))
    packets_sent += 1
print(f"Packets sent {packets_sent}")


