from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
import boto3
import os
from src.api.routersvoice import router as router_voice  # Importar router de voz
from src.api import main_router  # Importar router principal

app = FastAPI()

# Configurar variables AWS desde entorno
bucket_name = os.getenv("AWS_BUCKET_NAME")
region = os.getenv("AWS_REGION")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

# Configurar cliente S3
s3 = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region
)

# Incluir routers principales y de voz
app.include_router(main_router.router)
app.include_router(router_voice)  # Puedes quitar esta línea si main_router ya incluye el router_voice

@app.get("/", response_class=HTMLResponse)
async def main():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Subida de Archivos a Luzia</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Poppins', sans-serif; background-color: #f8f9fa; margin: 0; padding: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; }
            .container { background-color: #fff; padding: 20px 40px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center; max-width: 400px; width: 90%; }
            h1 { color: #9c7e3c; }
            .logo { width: 100px; margin-bottom: 15px; }
            input[type="file"] { margin: 10px 0; }
            button { background-color: #3ca776; color: white; border: none; padding: 10px 20px; border-radius: 25px; cursor: pointer; transition: background-color 0.3s; font-size: 16px; }
            button:hover { background-color: #2e8b5e; }
            @media (max-width: 600px) { .container { padding: 15px 20px; } .logo { width: 80px; } }
        </style>
    </head>
    <body>
        <div class="container">
            <img src="https://URL_DEL_LOGO_LUCIA" alt="Logo Lucía" class="logo">
            <h1>Bienvenido a Luzia</h1>
            <form id="upload-form" enctype="multipart/form-data">
                <input type="file" id="file" name="archivos" multiple><br>
                <button type="button" onclick="uploadFiles()">Subir archivos</button>
            </form>
            <p id="status"></p>
        </div>
        <script>
            async function uploadFiles() {
                const formData = new FormData();
                const files = document.getElementById('file').files;
                for (let i = 0; i < files.length; i++) {
                    formData.append("archivos", files[i]);
                }
                const response = await fetch('/subir', { method: 'POST', body: formData });
                const result = await response.json();
                document.getElementById('status').innerHTML = "<span style='color:green;font-weight:bold'>✅ Archivos subidos correctamente a S3</span>";
            }
        </script>
    </body>
    </html>
    """

@app.post("/subir")
async def upload(archivos: list[UploadFile] = File(...)):
    for archivo in archivos:
        contenido = await archivo.read()
        s3.put_object(Bucket=bucket_name, Key=archivo.filename, Body=contenido)
    return JSONResponse(content={"mensaje": "Archivos subidos correctamente a S3"})
