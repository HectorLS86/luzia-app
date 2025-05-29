from sqlalchemy.orm import Session
from . import models

# Crear un cliente
def create_cliente(db: Session, nombre: str, tipo_negocio: str, contacto: str):
    db_cliente = models.Cliente(nombre=nombre, tipo_negocio=tipo_negocio, contacto=contacto)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# Obtener clientes
def get_clientes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Cliente).offset(skip).limit(limit).all()

# Crear un documento
def create_documento(db: Session, nombre: str, tipo: str, categoria: str, cliente_id: int, ruta_archivo: str):
    db_documento = models.Documento(nombre=nombre, tipo=tipo, categoria=categoria, cliente_id=cliente_id, ruta_archivo=ruta_archivo)
    db.add(db_documento)
    db.commit()
    db.refresh(db_documento)
    return db_documento

# Obtener documentos
def get_documentos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Documento).offset(skip).limit(limit).all()
