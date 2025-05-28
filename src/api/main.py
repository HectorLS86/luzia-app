from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import boto3
import os

app = FastAPI()

# Cargar el nombre del bucket y credenciales desde variables de entorno
bucket_name = os.getenv("AWS_BUCKET_NAME")
region = os.getenv("AWS_REGION")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

# Configurar el cliente S3
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region
)

@app.get("/", response_class=HTMLResponse)
async def leer_raiz():
    return """
    <h1>Bienvenido a Luzia!</h1>
    <form action="/subir" enctype="multipart/form-data" method="post">
        <input name="archivos" type="file" multiple>
        <input type="submit" value="Subir">
    </form>
    """

@app.post("/subir")
async def subir_archivos(archivos: list[UploadFile] = File(...)):
    mensajes = []
    for archivo in archivos:
        contenido = await archivo.read()
        s3.put_object(Bucket=bucket_name, Key=archivo.filename, Body=contenido)
        mensajes.append(f"Archivo {archivo.filename} subido correctamente a S3!")
    return {"mensajes": mensajes}

