import datetime
import logging
import socket
import time
import collections

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
        self.message_queue = collections.deque()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, e_type, e_value, e_traceback):
        if e_type:
            LOGGER.error(f"{e_type} {e_value}")
        self.close()

    def check_for_data(self):
        self._rx_socket.setblocking(False)
        try:
            while True:
                message = self._rx_socket.recv(256)
                timestamp = datetime.datetime.now()
                print("retrieved message from socket")
                self.message_queue.append((message, timestamp))
        except BlockingIOError as e:
            print("no more messages from socket")
            pass

    def connect(self):
        if self._closed:
            self._rx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._closed = False
        try:
            self._rx_socket.bind((self.ip_addr, self.port))
            self._connected = True
            print("socket.bind() succeeded")
        except:
            print("socket.bind() failed")
            self._connected = False

    def close(self):
        self._closed = True
        self._rx_socket.close()

