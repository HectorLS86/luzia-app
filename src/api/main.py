    from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Permitir CORS para que el frontend pueda comunicarse con el backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto si necesitas limitar orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    saved_files = []
    upload_dir = "uploaded_files"
    os.makedirs(upload_dir, exist_ok=True)
    
    for file in files:
        file_location = f"{upload_dir}/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())
        saved_files.append(file_location)
    
    return JSONResponse(content={"message": "Archivos subidos exitosamente", "files": saved_files})

@app.get("/")
async def root():
    return {"message": "Hola desde Luzia"}
