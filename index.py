# lo primero es importar la libraria de Boto3
# Esta es una libraria que permite la comunicaion con cualquiera de los servicios de AWS a traves de API key y un usuario

import boto3

# Ahora se crea un cliente para el servicio se desea conectar.

#---------------- S3 --------------
s3_client = boto3.client(
    's3', # Nombre del servicio a conectar
    
    aws_access_key_id = '###########', # AWS Acces key ID
    
    aws_secret_access_key = '#######################3'
      
)

# -----  Colection ID
# Le podemos poner el nombre que querramos
# Este va a ser el nombre del data ste que se crea en el recognitioclearn service
# Va a tomar la information de los folderes de authorized users y crear un data set para compararlo con caras reales
# Este ID tambien se lo paso el e script de recognition
collectionId= 'faceRecognitionAuth'

#---------------- REKOGNITION SERVICE --------------
# Nos conectamos con el AWS recognition service.
rek_client = boto3.client(
    # Tener en cuenta que la palabra se escribe con K, asi en como lo reconoce AWS
    'rekognition', # Nombre del servicio a conectar
    
    aws_access_key_id = '##################', # AWS Acces key ID
    
    aws_secret_access_key = '#################################',
    
    # Es la region que tenemos dentro de AWS
    region_name = 'us-east-1'
          
)


#---------------- BUCKET --------------
# De aqui es don de va a cojer la informacion de los usuarios autorizados
bucket = 'auth-users-camping'

# auqi es donde voy a guardar todos los folders e imagenes disponibles en nuestro bucket
#
all_objects = s3_client.list_objects(Bucket =bucket)

#------------- CHEKC IF COLLECTION EXISTS AND REMOVE IT--------------------------------

# Vamos a revisar si los usuarios han sido agregados a alguna coleccion
# Si existe una colection borramos y creamos una nueva
# Resulve el problema si queremos borrar o agregar usuarios 
list_response = rek_client.list_collections(MaxResults = 2)
if collectionId in list_response['CollectionIds']:
    # Entonces aqui borramos la coleccion si existe
    # Es como ressetearse
    rek_client.delete_collection(CollectionId = collectionId)
    

#------------------- CREAR NUEVA COLECCION .-----------------

rek_client.create_collection(CollectionId = collectionId)

# Aqui hago un for loop para ir por los objetos
# Agrega todas las imagenens en el bucket a la cleccion y usa el folder con el nombre del usuario
# El nombre del usuario es el que agregamos cuando creamos el folder

for content in all_objects['Contents']:
    # aqui lo que estamos haciendo es que para cada folder lo separe por el slash
    # Asi se puede ir por cada uno por separado
    # Asi es como aparece en AWS
    # Esta codigo lo que hace es agrega las imagenens en la colection
    collection_name, collection_image = content['Key'].split('/')
    
    if collection_image:
        
        label = collection_name
        print('Indexing:', label)
        image = content['Key']
        
        index_response = rek_client.index_faces(
            CollectionId = collectionId,
            Image = {'S3Object': {'Bucket':bucket,'Name':image}},
            ExternalImageId=label,
            
            # Esta linea lo que hace es que revise una cara al mismo tiempo
            # Si hay multiples imagenens en la imagen solo busca una
            # Entonces se enfoca en una sola cara al mismo tiempo
            MaxFaces = 1,
            # Esto es para hacer un filtrado de la imagen
            QualityFilter = 'AUTO',
            # 
            #DetectionAttributes = ['DEFAULT']   
            DetectionAttributes = ['ALL'] 
        )

        # Los de arriba lo que hizo fue agregar todos los atributos a mi coleccion
        # Aqui me muestra cada imagen desdtro de cada bucket.
        print('FaceId:', index_response['FaceRecords'][0]['Face']['FaceId'])
