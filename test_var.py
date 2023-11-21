import argparse
import paho.mqtt.client as mqtt
import json

# Parse command-line arguments
parser = argparse.ArgumentParser(description='MQTT Publisher Script')
parser.add_argument('--captured_image', type=str, help='Captured Image Path', required=True)
parser.add_argument('--username', type=str, help='Username', required=True)
parser.add_argument('--similarity', type=float, help='Similarity value', required=True)
parser.add_argument('--confidence', type=float, help='Confidence value', required=True)
args = parser.parse_args()

# Create a message dictionary with the received data
message = {
    'captured_image': args.captured_image,
    'username': args.username,
    'similarity': args.similarity,
    'confidence': args.confidence
}

broker_address = "XX.16.1X9.XXX"
port = 1883
topic = "new_auth/Rp3/piCamera"
username = "mqtt"
password = "mqtt2023"

# Callback function for when the client connects to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to the MQTT broker")
        print("Attempting to publish to topic:", topic)
        # Publish the message after a successful connection
        client.publish(topic, json.dumps(message))
        print("Message published to topic:", topic)
        print("MESSAGE", json.dumps(message))
        # Disconnect after publishing
        client.disconnect()

    else:
        print("Connection failed with result code " + str(rc))

client = mqtt.Client("raspi-client")

# Set the username and password for authentication
client.username_pw_set(username, password)

# Assign the on_connect callback
client.on_connect = on_connect

# Connect to the MQTT broker
client.connect(broker_address, port, 60)

# Start the client loop
client.loop_forever()
