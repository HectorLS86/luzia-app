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
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region
)

@app.get("/", response_class=HTMLResponse)
async def leer_raiz():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Bienvenido a Luzia</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container py-5">
            <h1 class="text-center mb-4">🌟 Bienvenido a Luzia 🌟</h1>
            <div class="card p-4 shadow-sm">
                <form action="/subir" enctype="multipart/form-data" method="post">
                    <div class="mb-3">
                        <label for="archivos" class="form-label">Selecciona los archivos:</label>
                        <input name="archivos" id="archivos" type="file" class="form-control" multiple>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Subir archivos</button>
                </form>
            </div>
            <p class="text-center mt-3"><i>Puedes mantener pulsado Ctrl (o Cmd en Mac) para seleccionar múltiples archivos.</i></p>
        </div>
    </body>
    </html>
    """

@app.post("/subir")
async def subir_archivos(archivos: list[UploadFile] = File(...)):
    mensajes = []
    for archivo in archivos:
        contenido = await archivo.read()
        s3.put_object(Bucket=bucket_name, Key=archivo.filename, Body=contenido)
        mensajes.append(f"{archivo.filename} subido correctamente a S3!")
    return {"mensajes": mensajes}
