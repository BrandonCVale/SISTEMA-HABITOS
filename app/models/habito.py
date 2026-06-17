"""
Módulo de Modelo de Hábito.

Este módulo define la entidad 'Habito', la cual representa las actividades
que un usuario desea rastrear y monitorear en el sistema.
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey, Text, Boolean, Integer

from app import db


class Habito(db.Model):
    """
        Representa un hábito creado por un usuario.

        Attributes:
            id (int): Identificador único del hábito. Auto incrementable
            usuario_id (int): Clave foránea que vincula el hábito a su creador. [ref: > usuarios.id]
            nombre (str): Nombre corto del hábito (ej. 'Leer', 'Correr').
            descripcion (str, opcional): Detalles adicionales sobre el hábito.
            dias_semana (str): Días que va a realizar el hábito. Ej.: "L, M, X, J, V, S, D"
            fecha_creacion (datetime): Fecha en que se registró el hábito. Automática
            activo (bool): Para saber si el hábito sigue activo o el usuario decidió descansar de ese hábito
            racha_actual (int): Días consecutivos actuales en los que se ha completado el hábito sin fallar.
            mejor_racha (int): El récord histórico de más días consecutivos completando el hábito.
            horario (str, opcional): Momento del día sugerido para realizarlo (ej. 'Mañana', 'Tarde', 'Noche').
            dueno (Usuario): Objeto del usuario propietario de este hábito.
            registros (List[RegistroHabito]): Historial de los días en que se ha completado este hábito.
        """

    # Nombre de la tabla en la base de datos
    __tablename__ = 'habitos'

    # ============ Columnas de la tabla ============
    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # Clave foránea para conectar con la tabla usuarios
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    # Optional[] indica que este campo puede estar vacío (NULL en la base de datos)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # Guardará los días como un texto, ej: "L,M,X,J,V,S,D"
    dias_semana: Mapped[str] = mapped_column(String(20), nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    racha_actual: Mapped[int] = mapped_column(Integer, default=0)
    mejor_racha: Mapped[int] = mapped_column(Integer, default=0)
    horario: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # Relación inversa: Permite acceder al objeto Usuario desde un objeto Habito
    dueno: Mapped["Usuario"] = relationship("Usuario", back_populates="habitos")

    # Conexión al historial: Permite ver todos los registros de este hábito
    registros: Mapped[List["RegistroHabito"]] = relationship("RegistroHabito",
                                                             back_populates="habito",
                                                             cascade="all, delete-orphan")
