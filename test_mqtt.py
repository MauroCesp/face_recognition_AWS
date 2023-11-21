import paho.mqtt.client as mqtt
import json  # Import the json module
import datetime

# Get the current date and time
current_datetime = datetime.datetime.now()

# Format the date and time as a string
formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

broker_address = "50.X6.1X9.XXX"
port = 1883
topic = "new_auth/Rp3/piCamera"
username = "mqtt"
password = "mqtt2023"

auth_code = "mcespedes"

clientID = f"rp3/auth/{auth_code}"


rek_result = {
    'message': "Hello, ",
    'similarity': "99999999",
    'confidence': "hjhkhkj"
}



message = {
    'client_id': clientID,
    'message': rek_result,
    'date': formatted_datetime,
    'auth': "hjhkhkj"
}

# Callback function for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to the MQTT broker")
        # Publish the message after a successful connection
        client.publish(topic, json.dumps(message))
        print("Message published to topic: " + topic)
        print("MESSAGE" + json.dumps(message))

        # Stop the client loop
        client.loop_stop()

    else:
        print("Connection failed with result code " + str(rc))

client = mqtt.Client("raspi-client")

# Set the username and password for authentication
client.username_pw_set(username, password)

# Assign the on_connect callback
client.on_connect = on_connect

# Connect to the broker
client.connect(broker_address, port, 60)

# Start the client loop in a separate thread
client.loop_start()

# Keep the script running for a short time to allow the message to be published
try:
    import time
    time.sleep(2)  # Sleep for 2 seconds
except KeyboardInterrupt:
    pass

# Disconnect from the broker and exit the script
client.disconnect()
