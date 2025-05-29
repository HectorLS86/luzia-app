from pydantic import BaseModel
from typing import Optional

# Esquema para Cliente
class ClienteBase(BaseModel):
    nombre: str
    tipo_negocio: str
    contacto: str

class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int

    class Config:
        orm_mode = True

# Esquema para Documento
class DocumentoBase(BaseModel):
    nombre: str
    tipo: str
    categoria: str
    cliente_id: int
    ruta_archivo: str

class DocumentoCreate(DocumentoBase):
    pass

class Documento(DocumentoBase):
    id: int

    class Config:
        orm_mode = True
