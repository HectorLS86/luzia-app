from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
from datetime import datetime

class Documento(Base):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    tipo = Column(String, index=True)  # 'factura', 'receta', etc.
    cliente = Column(String, index=True)
    fecha = Column(DateTime, default=datetime.utcnow)
    ruta_archivo = Column(String)
