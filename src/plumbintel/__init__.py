"""
Program to coordinate communication between MQTT broker and SQL
    Server for PlumbInteligent System.
"""
import logging
import collections

Message = collections.namedtuple("Message", ["contents", "timestamp"])

#Logging set-up
LOGGER = logging.getLogger("PLUMBINTEL")
LOG_FORMAT = "{asctime} - {name} - {module:>8}:{lineno:>3} - {levelname:^8} - {message}"
FORMATTER = logging.Formatter(fmt=LOG_FORMAT, style="{")
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(CONSOLE_HANDLER)
LOGGER.setLevel(logging.INFO)

#Constants for establishing connections
CONF_PATH = "/etc/plumbintel.conf"

