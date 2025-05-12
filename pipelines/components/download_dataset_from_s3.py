from kfp import dsl
from kfp.components import create_component_from_func

@dsl.component(base_image='python:3.9-slim')
def download_dataset_from_s3(
    bucket_name: str,
    object_key: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    region: str = 'us-east-1',
    output_path: str = 'data/dataset.zip'
):
    import os
    import boto3
    import zipfile

    # Crear directorio si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Crear cliente S3
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )

    # Descargar archivo
    print(f"Descargando s3://{bucket_name}/{object_key} -> {output_path}")
    s3.download_file(bucket_name, object_key, output_path)

    # Descomprimir si es .zip
    if output_path.endswith(".zip"):
        with zipfile.ZipFile(output_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(output_path))
        print("Descompresión completada")

