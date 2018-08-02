import paho.mqtt.publish as publish

msgs = [("TEST", "msg{i}", 0, False) for i in range(0, 10000)]
num_msgs = len(msgs)
publish.multiple(msgs, hostname="18.217.132.144", port=1883)
print(f"Published {num_msgs} messages")
