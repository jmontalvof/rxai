import boto3
import os

# Configura tus credenciales de AWS (puede venir de variables de entorno o IAM role)
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name='us-east-1'  # ajusta si usas otra región
)

# Parámetros del dataset
dataset_bucket = 'rxai-datasets'
dataset_key = 'dataset.zip'
destination_path = 'data/dataset.zip'

# Crear carpeta destino si no existe
os.makedirs('data', exist_ok=True)

# Descargar archivo desde S3
print(f"Descargando {dataset_key} desde el bucket {dataset_bucket}...")
s3.download_file(dataset_bucket, dataset_key, destination_path)
print("Descarga completada.")

# (opcional) Descomprimir si es ZIP
import zipfile
if destination_path.endswith(".zip"):
    with zipfile.ZipFile(destination_path, 'r') as zip_ref:
        zip_ref.extractall('data/')
    print("Archivo descomprimido en carpeta data/")

