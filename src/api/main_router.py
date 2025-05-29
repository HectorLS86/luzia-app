from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas, database

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta para crear un cliente
@router.post("/clientes/", response_model=schemas.Cliente)
def create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    return crud.create_cliente(db=db, **cliente.dict())

# Ruta para obtener todos los clientes
@router.get("/clientes/", response_model=list[schemas.Cliente])
def read_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_clientes(db, skip=skip, limit=limit)

# Ruta para crear un documento
@router.post("/documentos/", response_model=schemas.Documento)
def create_documento(documento: schemas.DocumentoCreate, db: Session = Depends(get_db)):
    return crud.create_documento(db=db, **documento.dict())

# Ruta para obtener todos los documentos
@router.get("/documentos/", response_model=list[schemas.Documento])
def read_documentos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_documentos(db, skip=skip, limit=limit)
