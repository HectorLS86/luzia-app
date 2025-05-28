from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
import boto3
import os

app = FastAPI()

# Configurar S3 con variables de entorno
bucket_name = os.getenv("AWS_BUCKET_NAME")
region = os.getenv("AWS_REGION")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

s3 = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region
)

@app.get("/", response_class=HTMLResponse)
async def leer_raiz():
    return """
    <html>
        <head>
            <title>Luzia</title>
        </head>
        <body>
            <h1>🌞 Bienvenido a Luzia 🌞</h1>
            <form id="uploadForm" enctype="multipart/form-data">
                <p>Selecciona los archivos:</p>
                <input name="archivos" type="file" multiple>
                <button type="button" onclick="subirArchivos()">Subir archivos</button>
            </form>
            <div id="resultado"></div>
            <script>
                async function subirArchivos() {
                    const form = document.getElementById('uploadForm');
                    const formData = new FormData(form);
                    const response = await fetch('/subir', {
                        method: 'POST',
                        body: formData
                    });
                    const result = await response.json();
                    document.getElementById('resultado').innerText = result.mensajes.join('\\n');
                }
            </script>
            <p><i>Puedes mantener pulsado Ctrl (o Cmd en Mac) para seleccionar múltiples archivos.</i></p>
        </body>
    </html>
    """

@app.post("/subir")
async def subir_archivos(archivos: list[UploadFile] = File(...)):
    mensajes = []
    for archivo in archivos:
        contenido = await archivo.read()
        s3.upload_fileobj(
            Fileobj=bytes(contenido),
            Bucket=bucket_name,
            Key=archivo.filename
        )
        mensajes.append(f"{archivo.filename} subido correctamente a S3!")
    return JSONResponse(content={"mensajes": mensajes})
