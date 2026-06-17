"""
Módulo de inicialización de los modelos.

Este archivo permite exportar las clases Usuario y Habito para que puedan
ser importadas más fácilmente desde otras partes del sistema usando:
'from app.models import Usuario, Habito'
"""

from .usuario import Usuario
from .habito import Habito
from .registro_habito import RegistroHabito
# from app.models.usuario import Usuario
# from app.models.habito import Habito