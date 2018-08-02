import argparse
import paho.mqtt.publish as publish

parser = argparse.ArgumentParser(description="Send invalid payloads to the Network Interface")
parser.add_argument("topic", type=str)
args = parser.parse_args()

print("\n************************************************************")
payload = """["bad json", 1234"""
print("Case 1: Bad JSON format, payload = {payload}")
publish.single(args.topic, payload, hostname="18.217.132.144")
print("Verify that an error was logged by plumbintel then press <Enter>", end="")
input()

print("\n************************************************************")
payload = """["bad data type", "I'm bad"]"""
print("Case 2: Bad data type, payload = {payload}")
publish.single(args.topic, payload, hostname="18.217.132.144")
print("Verify that an error was logged by plumbintel then press <Enter>", end="")
input()

print("\n************************************************************")
payload = """["value", 1234, "one too many"]"""
print("Case 3: bad packet length, payload = {payload}")
publish.single(args.topic, payload, hostname="18.217.132.144")
print("Verify that an error was logged by plumbintel then press Enter", end="")
input()

