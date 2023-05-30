
# Importamos esta libreria para poder correr el script de recognition en el backgroud
import subprocess

# Con esta libreria podemos hacer cosas en el sistema y conectar perifericos
import sys

import os

import gpiozero
# Esta es la libreria que vamos a usar se puede usar la GPIO
from gpiozero import LED


from gpiozero import Button


from time import sleep


#----------- CREATE LEDS VARIABLES --------------------------------

#--------- LEDS -------------------
# Creo los pines que deseo trabajar
yellow_led = LED(19)
red_led = LED(24)

# ----------- RELAY -----------------
# Inicializa PIN relacionado con el relay
relay_pin = 17

#------------Button SENSOR --------------
button_push = Button(22)

# Lo inicializamos como HIG para que la puerta este cerrada

# Depende de lo que queramos hacer lo dejamos HIGH or LOW
relay = gpiozero.OutputDevice(relay_pin, active_high = True, initial_value = False )


def access_auth():
    
    # aqui voy a correr este comando para que ejecute el archivo de recognition y me guarde el output
    return_text = subprocess.check_output('python3 recognition.py', shell = True, universal_newlines=True)
    print(return_text)
    
    # Vamos a jugar con la palabra que viene solomanete dentro del mensaje si un usario a sido reconocido
    # La palabra Hello solo llega si el usuario esta authorizado.
    if 'Hello' in return_text:
        
        print('Usuario es autorizado')
        
        yellow_led.on()
        # Este es el tiempo que deseamos tenenr el LED encendido
        # Se puede usar para cualquier 
        
        # Cambia el estado del realy
        relay.on()
        sleep(10)
        
        yellow_led.off()
        
        # El relay vuelve al estado original
        relay.off()
        
    else:       
        print('Unauthorized user')
        
        red_led.on()
        sleep(10)
        
        

# Ahora aqui lo que hacemos es un while para que se quede a la escucha de si el boton es presionado
# Eventualmente quiero sustituir ese somando por una intruccion desde el movil o la apicacion web
# Pero mejor seria un sensor que detecte que llego la persona para que tenga una experiencia máspersonalizaa¡da.

while True:
    
    # Este mecanismo es simple 
    # Si el boton está presionado comienza el ciclo de identificacion.
    if button_push.is_pressed:
        print('button is pressed')
        access_auth()