"""
Program to coordinate communication between MQTT broker and SQL
    Server for PlumbInteligent System.
"""
import logging

#Logging set-up
LOGGER = logging.getLogger("PLUMBINTEL")
LOG_FORMAT = "{asctime} - {name} - {filename}:{lineno} - {levelname} - {message}"
FORMATTER = logging.Formatter(fmt=LOG_FORMAT, style="{")
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(CONSOLE_HANDLER)
LOGGER.setLevel(logging.DEBUG)

#Constants for establishing connections
CONF_PATH = "/etc/plumbintel.conf"

