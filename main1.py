
# Importamos esta libreria para poder correr el script de recognition en el backgroud
import subprocess

# Con esta libreria podemos hacer cosas en el sistema y conectar perifericos
import sys

import json

import os

import gpiozero
# Esta es la libreria que vamos a usar se puede usar la GPIO
from gpiozero import LED


from gpiozero import Button


from time import sleep


#----------- CREATE LEDS VARIABLES --------------------------------

#--------- LEDS -------------------
# Creo los pines que deseo trabajar
yellow_led = LED(18)
red_led = LED(17)

# Define variables to store the results
captured_image = ""
username = ""
similarity = 0.0
confidence = 0.0

def access_auth():
    global captured_image, username, similarity, confidence

    # Run the recognition script and capture the output
    return_text = subprocess.check_output('python3 recognition.py', shell=True, universal_newlines=True)

    # Print the captured text
    # print(return_text)

    # Split the lines and extract values
    lines = return_text.strip().split('\n')
    if len(lines) >= 4:
        captured_image = lines[0].split('Captured:')[1].strip()
        username = lines[1].split('Hello, ')[1].strip()
        similarity = float(lines[2].split('Similarity: ')[1].strip())
        confidence = float(lines[3].split('Confidence: ')[1].strip())

        if 'Hello' in lines[1]:

             # ---------------------------------------------------- #
            #                   MQTT: envio info
            # ---------------------------------------------------- #   
            #         
            # Call the MQTT publisher script with the extracted variables
            publisher_script = 'python test_var.py'
            # Esta es la forma como le paso los parametro del script recognition a este.
            # Le asigno las variables y el otr script las recoge y las evia por Mqtt
            command = f"{publisher_script} --captured_image '{captured_image}' --username '{username}' --similarity {similarity} --confidence {confidence}"
            subprocess.call(command, shell=True)

            # ---------------------------------------------------- #
            #                   ACTIONS: ejecuto acciones
            # ---------------------------------------------------- #
            print('User is authorized')
            print(lines[2])
            print(lines[3])
            yellow_led.on()
            sleep(10)
            yellow_led.off()

        else:
            print('Unauthorized user')
            red_led.on()
            sleep(10)
    else:
        print('Error: Unexpected output format')
        publisher_script = 'python test_var.py'
        command = f"{publisher_script} --captured_image 'tradicion' --username 'trabajo' --similarity {similarity} --confidence {confidence}"
        subprocess.call(command, shell=True)



access_auth()

# Now you can use the captured variables (captured_image, username, similarity, confidence) for MQTT or other purposes.
# This code splits the lines of the printed output and extracts the values directly from each line, allowing you to use the captured variables as needed.





