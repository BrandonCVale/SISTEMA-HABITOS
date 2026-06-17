"""
Módulo de Repositorio de Usuarios.

Implementa el Patrón Repositorio (RNF-01) para separar la lógica de acceso
a datos de los controladores web. Se encarga de guardar y buscar usuarios.
"""

import bcrypt
from typing import Optional
from app import db
from app.models.usuario import Usuario


class UsuarioRepository:
    """
        Clase que encapsula todas las consultas a la base de datos
        relacionadas con la entidad Usuario.
    """

    @staticmethod
    def crear_usuario(correo: str, contrasena_plana: str, nombre_usuario: str) -> Usuario:
        """
        Crea un nuevo usuario en la base de datos con contraseña encriptada (RNF-06).
        Args:
            correo (str): El correo del nuevo usuario.
            contrasena_plana (str): La contraseña real introducida por el usuario.
            nombre_usuario (str): El nombre de usuario elegido.
        Returns:
            Usuario: El objeto del usuario recién guardado en la base de datos.
        """

        # Encriptar la constrasena
        # Genera un texto aleatorio
        salt = bcrypt.gensalt()
        hash_contrasena = bcrypt.hashpw(contrasena_plana.encode('utf-8'), salt)

        # Crear el objeto Usuario con el hash
        # Decodificamos el hash a string para guardarlo en la BD
        nuevo_usuario = Usuario(correo=correo,
                                contrasena=hash_contrasena.decode('utf-8'),
                                nombre_usuario=nombre_usuario)

        # Guardamos en la BD
        # Inserta pero no guarda
        db.session.add(nuevo_usuario)
        # Guarda los cambios
        db.session.commit()

        return nuevo_usuario

    @staticmethod
    def obtener_usuario_por_correo(correo: str) -> Optional[Usuario]:
        """
        Busca un usuario en la base de datos utilizando su correo electrónico.
        Utiliza la sintaxis moderna de SQLAlchemy 2.0.
        Args:
            correo (str): El correo a buscar.
        Returns:
            Usuario o None: Retorna el usuario si existe, o None si no se encuentra.
        """

        # Consulta
        consulta = db.select(Usuario).where(Usuario.correo == correo)

        # Ejecutamos la consulta pidiendo solo un resultado o ninguno
        resultado = db.session.execute(consulta).scalar_one_or_none()
        return resultado

    @staticmethod
    def verificar_credenciales(correo: str, contrasena_plana: str) -> Optional[Usuario]:
        """
        Verifica si el correo existe y si la contraseña coincide.
        Args:
            correo (str): Correo del usuario que intenta ingresar.
            contrasena_plana (str): Contraseña que el usuario escribió en el login.
        Returns:
            Usuario si las credenciales son correctas, None si fallan.
        """
        # 1. Buscar al usuario en la BD por su correo
        usuario = UsuarioRepository.obtener_usuario_por_correo(correo)
        if not usuario:
            return None  # El correo no existe

        # 2. Comparamos la contrasena plana con el hash guardado en la BD
        # IMPORTANTE: bcrypt.checkpw requiere que ambos textos estén en formato 'bytes'
        contrasena_bytes = contrasena_plana.encode('utf-8')
        hash_bytes = usuario.contrasena.encode('utf-8')

        if bcrypt.checkpw(contrasena_bytes, hash_bytes):
            return usuario  # Credenciales correctas
        return None  # Contraseña incorrecta
