from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

# Crea la carpeta de uploads si no existe
os.makedirs("uploads", exist_ok=True)

@app.get("/")
async def read_root():
    return {"message": "Hola desde Luzia"}

@app.post("/upload/")
async def upload_files(files: list[UploadFile] = File(...)):
    saved_files = []
    for file in files:
        contents = await file.read()
        file_path = os.path.join("uploads", file.filename)
        with open(file_path, "wb") as f:
            f.write(contents)
        saved_files.append(file.filename)
    return {"message": f"Se han subido los archivos: {', '.join(saved_files)}"}

@app.get("/ui", response_class=HTMLResponse)
async def read_ui():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Sube tus documentos</title>
    </head>
    <body>
        <h1>Bienvenido a Luzia!</h1>
        <form action="/upload/" enctype="multipart/form-data" method="post">
            <input name="files" type="file" multiple>
            <input type="submit" value="Subir">
        </form>
    </body>
    </html>
    """
