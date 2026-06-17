"""
Módulo de Modelo de Registro de Hábito.

Este módulo define la entidad 'RegistroHabito', la cual funciona como
el historial diario para saber qué días se completó un hábito específico.
"""

from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Boolean, Date, UniqueConstraint

from app import db


class RegistroHabito(db.Model):
    """
    Representa el registro diario de un hábito.
    
    Attributes:
        id (int): Identificador único del registro.
        habito_id (int): Clave foránea que conecta este registro con su hábito padre.
        fecha (date): La fecha exacta (día, mes, año) a la que corresponde este registro.
        completado (bool): Indica si el hábito fue marcado como hecho en esa fecha.
        habito (Habito): Objeto del hábito al que pertenece este registro (Relación).
    """
    __tablename__ = 'registro_habitos'

    # REGLA DE ORO: Un usuario no puede completar el MISMO hábito dos veces el MISMO día
    __table_args__ = (
        UniqueConstraint('habito_id', 'fecha', name='uq_habito_fecha_diaria'),
    )

    # =========== COLUMNAS DE LA TABLA =============
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    habito_id: Mapped[int] = mapped_column(ForeignKey("habitos.id"), nullable=False)

    # Usamos Date (sin hora) para que coincida exactamente con los días del calendario
    fecha: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)

    # Estado del registro
    completado: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relación inversa para llegar al hábito desde el registro
    habito: Mapped["Habito"] = relationship("Habito", back_populates="registros")
