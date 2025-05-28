from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hola desde Luzia"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    return {"filename": file.filename, "content": content.decode("utf-8")}

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
            <input name="file" type="file">
            <input type="submit" value="Subir">
        </form>
    </body>
    </html>
    """
