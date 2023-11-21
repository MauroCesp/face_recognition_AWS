import paho.mqtt.client as mqtt

broker_address = "50.16.189.156"
port = 1883
topic = "new_auth/Rp3/piCamera"
username = "mqtt"
password = "mqtt2023"

# Callback function for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to the MQTT broker")
        # Subscribe to the specified topic
        client.subscribe(topic)
        print("Subscribed to topic: " + topic)
    else:
        print("Connection failed with result code " + str(rc))

# Callback function for when a message is received
def on_message(client, userdata, message):
    print("Received message on topic: " + message.topic)
    print("Message: " + str(message.payload))  # Print the payload as a string

client = mqtt.Client("raspi-client2")

# Set the username and password for authentication
client.username_pw_set(username, password)

# Assign the on_connect and on_message callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(broker_address, port, 60)

# Start the client loop (blocks the script)
client.loop_forever()
