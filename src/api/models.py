from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    tipo_negocio = Column(String, index=True)  # Tipo de negocio: pastelería, fotografía, etc.
    contacto = Column(String, index=True)      # Información de contacto (opcional)

    documentos = relationship("Documento", back_populates="cliente")


class Documento(Base):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)              # Nombre del archivo
    tipo = Column(String, index=True)                # Tipo del documento: factura, receta, etc.
    categoria = Column(String, index=True)           # Categoría: pedidos, contratos, etc.
    fecha = Column(DateTime, default=datetime.utcnow)
    ruta_archivo = Column(String, index=True)        # Ruta completa en S3
    cliente_id = Column(Integer, ForeignKey("clientes.id"))

    cliente = relationship("Cliente", back_populates="documentos")
