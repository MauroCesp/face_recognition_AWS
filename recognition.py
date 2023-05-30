from picamera import PiCamera

import time 
import boto3

# Ahora voy a conectar el folder donde voy a guardar las imagenes que tome la picamera
directory = '/home/pi/Desktop/face-recognition-project/faces'

#------------ Creo el objeto de la camera --------
p = PiCamera()
# Seteo la resolucion de la camera
p.resolution=(800,600)
p.start_preview()

# Proveo el ID del servicio de rekognition de AWS
# Esto lo compiamos del otro archivo del index
# El el nombre que le di a la coleccion en el servicio de recognition de AWS
collectionId= 'faceRecognitionAuth'

# Tambien necesitamos copiar el path para conectarnos al servicio
# Para comparar las imagenens que copiamos de la camera con las que tenenmos en la colleccion de caras autorizadas

#---------------- REKOGNITION SERVICE --------------
# Nos conectamos con el AWS recognition service.
rek_client = boto3.client(
    # Tener en cuenta que la palabra se escribe con K, asi en como lo reconoce AWS
    'rekognition', # Nombre del servicio a conectar
    
    aws_access_key_id = '················', # AWS Acces key ID
    
    aws_secret_access_key = '···························',
    
    # Es la region que tenemos dentro de AWS
    region_name = 'us-east-1'
          
)


# ------------------ MAIN --------------------------------

if __name__ == '__main__':
    
    # Pongo un sleep de dos segudos para esperar que la camera se inicie bien
    time.sleep(2)
    
    # Necesito crear cada imagen que tome la camera con un nombre diferente
    # SI la guardo con el mismo nombre cada vez la imagen se sobreescribe y no tendre el data set completo de las imagenens que se han tomado
    
    # It will get the current time y lo mutiplico por 1000 para que cree random numbrers
    # Este es el nombre de la imagen
    milli = int(round(time.time()*1000))
              
    image = '{}/image_{}.jpg'.format(directory,milli)
    
    # Ahora tomo la foto y la guardo en ese directorio, con ese nombre
    p.capture(image)
    
    print('Captured:'+ image)
    
    with open(image,'rb') as image:
        try:
            match_response = rek_client.search_faces_by_image(CollectionId = collectionId,
                                                              Image = {'Bytes':image.read()},
                                                              MaxFaces = 1,
                                                              FaceMatchThreshold=85)
            if match_response['FaceMatches']:
                print('Hello, ', match_response['FaceMatches'][0]['Face']['ExternalImageId'])
                
                print('Similarity:', match_response['FaceMatches'][0]['Similarity'])
                
                print('Confidence:', match_response['FaceMatches'][0]['Face']['Confidence'])
            else:
                print('No Faces Match')
        except Exception as e:
            print('No Faces Detected in de Image', e)
            
        time.sleep(1)
        
        
