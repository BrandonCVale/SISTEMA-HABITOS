"""
Módulo de Repositorio de Hábitos.

Encapsula la lógica de acceso a datos para la entidad Habito.
"""

import calendar
from datetime import date
from typing import List, Optional
from app import db
from app.models.habito import Habito
from app.models.registro_habito import RegistroHabito


class HabitoRepository:

    @staticmethod
    def obtener_habitos_por_usuario(usuario_id: int, estado: str = 'todos') -> List[Habito]:
        """
        Busca todos los hábitos que pertenecen a un usuario específico.
        Permite filtrar por estado ('todos', 'activos', 'inactivos').
        """
        # Consulta moderna de SQLAlchemy 2.0
        consulta = db.select(Habito).where(Habito.usuario_id == usuario_id)

        # Agregamos filtros extra dependiendo de lo que pida la ruta
        if estado == 'activos':
            consulta = consulta.where(Habito.activo == True)
        elif estado == 'inactivos':
            consulta = consulta.where(Habito.activo == False)

        # .scalars().all() devuelve la lista de objetos listos para usar
        return db.session.execute(consulta).scalars().all()

    @staticmethod
    def obtener_habito_por_id(habito_id: int) -> Optional[Habito]:
        """
        Busca un hábito específico por su ID.
        """
        return db.session.get(Habito, habito_id)

    @staticmethod
    def crear_habito(nombre: str,
                     usuario_id: int,
                     dias_semana: str,
                     descripcion: Optional[str] = None) -> Habito:
        """
        Guarda un nuevo hábito en la base de datos asociado a un usuario específico.
        """
        nuevo_habito = Habito(
            nombre=nombre,
            descripcion=descripcion,
            usuario_id=usuario_id,
            dias_semana=dias_semana
        )

        db.session.add(nuevo_habito)
        db.session.commit()

        return nuevo_habito

    @staticmethod
    def editar_habito(habito_id: int,
                      nombre: str,
                      descripcion: Optional[str],
                      dias_semana: str,
                      activo: bool) -> Optional[Habito]:
        """
        Edita un hábito existente en la base de datos.
        """
        # 1. Buscamos el hábito en la base de datos usando su ID
        habito = db.session.get(Habito, habito_id)

        # 2. Si el hábito no existe (quizás lo borraron), regresamos None
        if not habito:
            return None

        # 3. Actualizamos las propiedades del objeto con los nuevos datos
        habito.nombre = nombre
        habito.descripcion = descripcion
        habito.dias_semana = dias_semana
        habito.activo = activo

        # 4. Confirmamos los cambios en la base de datos
        db.session.commit()

        return habito

    @staticmethod
    def eliminar_habito(id_habito: int) -> None:
        """Elimina un habito en la BD
        """
        # Buscar el hábito en la BD (trae un objeto python de la clase Habito con sus atributos)
        habito = db.session.get(Habito, id_habito)

        # Validación
        # Si el hábito existe lo eliminamos
        if habito:
            db.session.delete(habito)
            db.session.commit()

    @staticmethod
    def marcar_completado_hoy(id_habito: int) -> bool:
        """
        Marca un hábito como completado en el día de hoy. 
        Si ya estaba completado, lo desmarca (toggle).
        Retorna True si se completó, False si se desmarcó.
        """
        hoy = date.today()  # ej. yyyy-mm-dd

        # Buscamos si ya existe un registro para hoy
        consulta = db.select(RegistroHabito).where(
            RegistroHabito.habito_id == id_habito,
            RegistroHabito.fecha == hoy
        )
        # Solo traemos 1 registro o None
        registro_existente = db.session.execute(consulta).scalar_one_or_none()
        
        # Obtenemos el hábito para poder modificar sus rachas
        habito = db.session.get(Habito, id_habito)

        # Si ya estaba completado
        if registro_existente:
            db.session.delete(registro_existente)
            # Si deshace la acción, le restamos 1 a su racha (evitando que baje de cero)
            habito.racha_actual = max(0, habito.racha_actual - 1)
            db.session.commit()
            return False  # Para avisar que acabamos de "apagar" o "desmarcar" el hábito.
        else:
            # Equivalente a; INSERT INTO registro_habitos (habito_id, fecha, completado) VALUES (5, '2026-06-10', True);
            # Lo que nos da un objeto Python
            nuevo_registro = RegistroHabito(habito_id=id_habito, fecha=hoy, completado=True)
            # Agregamos en la BD
            db.session.add(nuevo_registro)
            # Sumamos 1 a la racha
            habito.racha_actual += 1
            # Verificamos si rompió su récord histórico
            if habito.racha_actual > habito.mejor_racha:
                habito.mejor_racha = habito.racha_actual
            # Guardamos
            db.session.commit()
            return True

    @staticmethod
    def obtener_dias_activos_mes(usuario_id: int, anio: int, mes: int) -> set:
        """
        Obtiene los días específicos del mes en los que el usuario completó 
        al menos un hábito. Retorna un Set (conjunto) para búsquedas rápidas.

        Sirve para pintar el calendario de la página principal.
        """
        # Averiguamos cuántos días tiene este mes
        _, num_dias = calendar.monthrange(anio, mes)
        primer_dia = date(anio, mes, 1)
        ultimo_dia = date(anio, mes, num_dias)

        # Hacemos un JOIN para buscar solo los registros de este usuario en este mes
        consulta = db.select(RegistroHabito.fecha).join(Habito).where(
            Habito.usuario_id == usuario_id,
            RegistroHabito.fecha >= primer_dia,
            RegistroHabito.fecha <= ultimo_dia,
            RegistroHabito.completado == True
        )
        fechas = db.session.execute(consulta).scalars().all()

        # Extraemos solo el número del día (ej. 15) y lo metemos en un Set {}
        return {f.day for f in fechas}
