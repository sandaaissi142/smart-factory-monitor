import json
import time

import paho.mqtt.client as mqtt
from sensors import MachineSimulator

BROKER = "localhost"
PORT = 1883
TOPIC = "factory/M1/sensors"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT)
client.loop_start()

machine = MachineSimulator("M1")
print(f"Publication sur {TOPIC} (Ctrl+C pour arrêter)")

try:
    while True:
        data = machine.read()
        client.publish(TOPIC, json.dumps(data))
        print(data)
        time.sleep(0.5)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
    print("Arrêté.")