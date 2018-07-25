import logging
import sql
import udp
import json
import __init__ as plumbintel

LOGGER = logging.getLogger("PLUMBINTEL")

def parse_device_packet(packet):
    """Parse packets, convert voltage to correct form and return list for SQL DB.
        Plumbintel packets are expected to be in the following form:
        - "tuple(bytestring, datetime.datetime())"
          - bytestring: ["<device_id>", <voltage_reading>]
        Output:
        - list[str(device_id), int(evaluated_reading), str(timestamp)]
    """
    try:
        sql_payload = json.loads(message[0], encoding="utf-8")
        LOGGER.debug(f"payload: {payload}")
        return sql_payload
    except json.decoder.JSONDecodeError as error:
        LOGGER.error(f"received improperly formatted payload {str(message.payload)}")

def configure():
    """Configures all the necessary variables for operation.
        ***MUST BE RUN FIRST***
    """
    conf = None
    conf_path = plumbintel.CONF_PATH
    try:
        with open(conf_path, mode='r') as conf_file:
            conf = json.load(conf_file)
            LOGGER.info("Successfully read in conf_file")
            return conf
    except json.decoder.JSONDecodeError as e:
        LOGGER.critical(f"Could not parse config at {conf_path}.")
    except FileNotFoundError as e:
        LOGGER.critical(f"Could not find config as {conf_path}.")
    except PermissionError as e:
        LOGGER.critical(f"Could not open {conf_path}. Escalate Permissions.")
    raise Exception

def main(config):
    with sql.Database(**config["SQL"], timeout=30) as db:
        with udp.Listener(ip_addr=MQTT_BROKER_HOST,
                          port=MQTT_BROKER_PORT) as listener:
            while True:
                listener.check_for_data()

if __name__ == "__main__":
    config = configure()
    main(config)

