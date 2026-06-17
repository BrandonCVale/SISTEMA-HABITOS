"""
Módulo de Modelo de Usuario.

Este módulo define la entidad 'Usuario' para la base de datos, manejando
la información de autenticación y la relación con los hábitos creados.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime

from flask_login import UserMixin

from app import db


class Usuario(db.Model, UserMixin):
    """
        Representa a un usuario registrado en el sistema.

        Attributes:
            id (int): Identificador único del usuario (Clave Primaria).
            correo (str): Correo electrónico único del usuario.
            contrasena (str): Contraseña encriptada por seguridad.
            fecha_registro (datetime): Fecha y hora exacta en que se creó la cuenta.
            habitos (List[Habito]): Lista de hábitos que pertenecen a este usuario.
        """

    # Nombre de la tabla en la base de datos
    __tablename__ = 'usuarios'

    # Columnas de la tabla
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    correo: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    contrasena: Mapped[str] = mapped_column(String(128), nullable=False)
    nombre_usuario: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # Relación uno a muchos: Un usuario tiene multiples habitos
    # El type hint List["Habito"] indica que devolverá una lista de objetos de la otra clase.
    habitos: Mapped[List["Habito"]] = relationship("Habito",
                                                   back_populates="dueno",
                                                   cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """
        Representación en string del objeto, útil para depuración (debugging).
        """
        return f"<Usuario(id={self.id}, correo='{self.correo}')>"
