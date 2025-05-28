from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import boto3
import os

app = FastAPI()

# Configurar AWS S3
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
    <!DOCTYPE html>
    <html>
    <head>
        <title>Subida de Archivos a Luzia</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: #f4f4f4;
                padding-top: 50px;
            }
            h1 {
                color: #333;
            }
            .mensaje {
                display: none;
                margin-top: 20px;
                padding: 10px;
                background-color: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
                border-radius: 5px;
            }
            input[type="file"] {
                margin: 20px;
                padding: 10px;
                background-color: white;
                border-radius: 5px;
            }
            input[type="submit"] {
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            input[type="submit"]:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <h1>🌞 Bienvenido a Luzia 🌞</h1>
        <form id="uploadForm" enctype="multipart/form-data" method="post">
            <label>Selecciona los archivos:</label><br>
            <input name="archivos" type="file" multiple><br>
            <input type="submit" value="Subir archivos">
        </form>
        <div class="mensaje" id="mensajeExito">✅ Archivos subidos correctamente a S3</div>

        <script>
            const form = document.getElementById('uploadForm');
            const mensaje = document.getElementById('mensajeExito');
            form.addEventListener('submit', async (e) => {
                e.preventDefault();  // Evita recargar la página
                const formData = new FormData(form);
                const response = await fetch('/subir', {
                    method: 'POST',
                    body: formData
                });
                if (response.ok) {
                    mensaje.style.display = 'block';  // Muestra el mensaje
                    form.reset();  // Opcional: limpia los campos del formulario
                } else {
                    alert('❌ Error al subir los archivos.');
                }
            });
        </script>
    </body>
    </html>
    """

@app.post("/subir")
async def subir_archivos(archivos: list[UploadFile] = File(...)):
    for archivo in archivos:
        contenido = await archivo.read()
        s3.put_object(Bucket=bucket_name, Key=archivo.filename, Body=contenido)
    return {"mensaje": "Archivos subidos correctamente a S3"}
