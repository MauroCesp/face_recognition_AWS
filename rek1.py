from picamera import PiCamera
import paho.mqtt.client as mqtt
import time
import boto3
import json

# Directory to store captured images
directory = '/home/camping/Documents/aws/faces'

# Create a PiCamera object
p = PiCamera()
p.resolution = (800, 600)
p.start_preview()

# AWS Rekognition configuration
collectionId = 'faceRecognitionAuth'
rek_client = boto3.client(
    'rekognition',
    aws_access_key_id = '', # AWS Acces key ID',
    
    aws_secret_access_key = 'j',
    region_name='us-east-1'
)

# Capture an image and process it
def capture_and_process_image():
    # Capture an image
    milli = int(round(time.time() * 1000))
    image = '{}/image_{}.jpg'.format(directory, milli)
    p.capture(image)
    print('Captured:' + image)

    # Process the captured image using Rekognition
    with open(image, 'rb') as image_file:
        match_response = rek_client.search_faces_by_image(
            CollectionId=collectionId,
            Image={'Bytes': image_file.read()},
            MaxFaces=1,
            FaceMatchThreshold=85
        )

        if match_response['FaceMatches']:
            matched_face = match_response['FaceMatches'][0]
            external_image_id = matched_face['Face']['ExternalImageId']
            similarity = matched_face['Similarity']
            confidence = matched_face['Face']['Confidence']

            response = {
                'message': "Hello, " + external_image_id,
                'similarity': similarity,
                'confidence': confidence
            }

            # Publish the response back to the MQTT topic
            response_topic = "new_auth/Rp3/piCamera"
            client.publish(response_topic, json.dumps(response))
            print(response)

if __name__ == '__main__':
    broker_address = "XX.16.1X9.1XX"
    port = 1883
    topic = "new_auth/Rp3/piCamera"
    username = "mqtt"
    password = "mqtt2023"

    client = mqtt.Client("raspi-client")

    # Set the username and password
    client.username_pw_set(username, password)

    client.connect(broker_address, port, 60)

    # Loop to listen for messages and process the image
    client.loop_start()

    capture_and_process_image()  # Capture and process the image once

    # Terminate the script after processing
    client.loop_stop()
    client.disconnect()
