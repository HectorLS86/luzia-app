from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

# Crear la carpeta de uploads si no existe
os.makedirs('subidas', exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def leer_raiz():
    return """
    <h1>Bienvenido a Luzia!</h1>
    <form action="/subir" enctype="multipart/form-data" method="post">
        <input name="archivo" type="file">
        <input type="submit" value="Subir">
    </form>
    """

@app.post("/subir")
async def subir_archivo(archivo: UploadFile = File(...)):
    ruta = os.path.join("subidas", archivo.filename)
    with open(ruta, "wb") as buffer:
        contenido = await archivo.read()
        buffer.write(contenido)
    return {"mensaje": f"Archivo '{archivo.filename}' subido exitosamente!"}
