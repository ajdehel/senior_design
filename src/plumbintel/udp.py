import datetime
import logging
import socket
import time
import collections
import threading
from __init__ import Message

LOGGER = logging.getLogger("PLUMBINTEL")

class Listener:
    """Class to accept UDP messages coming from a given port."""

    def __init__(self, ip_addr="127.0.0.1", port=10000):
        if ip_addr is None:
            raise RuntimeError("IP Address must be specified")
        if type(port) is not int:
            raise TypeError("Port must be an int()")
        self.ip_addr = ip_addr
        self.port = port
        self._rx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._closed = True
        self._thread = None
        self._stopped = True
        self.message_queue = collections.deque()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, e_type, e_value, e_traceback):
        if self._thread.is_alive():
            self._stopped = True
            self._thread.join()
            LOGGER.info("Thread stopped")
        if e_type:
            LOGGER.error(f"{e_type} {e_value}")
        self.close()

    def __call__(self):
        if not self._connected:
            self.connect()
        while not self._stopped:
            self.check_for_data()

    def start_thread(self):
        self._thread = threading.Thread(target=self, name="SocketListener")
        self._stopped = False
        self._thread.start()
        LOGGER.info("Started listener thread.")

    def check_for_data(self):
        self._rx_socket.setblocking(False)
        packet_count = 0
        try:
            while True:
                packet = self._rx_socket.recv(256)
                timestamp = datetime.datetime.now()
                LOGGER.debug("Retrieved message from socket.")
                self.message_queue.append(Message(packet, timestamp))
                packet_count += 1
        except BlockingIOError as e:
            pass

    def connect(self):
        if self._closed:
            self._rx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._closed = False
        try:
            self._rx_socket.bind((self.ip_addr, self.port))
            self._connected = True
            LOGGER.info(f"Socket bound at {self.ip_addr}:{self.port}.")
        except:
            LOGGER.error("Failed to bind socket.")
            self._connected = False

    def close(self):
        self._closed = True
        self._rx_socket.close()

