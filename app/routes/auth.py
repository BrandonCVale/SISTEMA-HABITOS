"""
Módulo de Rutas de Autenticación.

Define los 'endpoints' (URL) para el registro, inicio y cierre de sesión
de los usuarios. Utiliza Blueprints para mantener el código modular.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError

from app.repositories.usuario_repository import UsuarioRepository

# CREAMOS EL BLUEPRINT AUTH
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    """
    Maneja la vista y el procesamiento del formulario de registro.

    - GET: Muestra la página HTML con el formulario.
    - POST: Recibe los datos del formulario, intenta crear el usuario en la base de datos y redirige según el resultado.
    """

    # Si el usuario ya tiene sesión iniciada, no tiene sentido que se registre de nuevo
    if current_user.is_authenticated:
        flash("Ya has iniciado sesión.", "success")
        return redirect(url_for('pag_principal.inicio'))

    # Si el usuario envió el formulario (POST)
    if request.method == 'POST':
        # Obtenemos los datos que el usuario escribió en el HTML
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        usuario = request.form.get('nombre_usuario')

        # Validaciones básicas de servidor (RNF-08)
        if not correo or not contrasena or not usuario:
            flash("Todos los campos son obligatorios.", "error")
            return redirect(url_for('auth.registro'))

        try:
            # Llamamos a nuestro Repositorio para que haga el trabajo pesado
            UsuarioRepository.crear_usuario(correo=correo, contrasena_plana=contrasena, nombre_usuario=usuario)

            # Si sale bien, mostramos un mensaje de éxito
            flash("¡Registro exitoso! Ahora puedes iniciar sesión.", "success")

            # Por ahora, los redirigimos al mismo formulario (luego será al login)
            return redirect(url_for('auth.registro'))

        except IntegrityError:
            # Si SQLAlchemy detecta que el correo o usuario ya existe (ambos son unique=True)
            flash("Este correo electrónico o nombre de usuario ya está registrado.", "error")
            return redirect(url_for('auth.registro'))

    # Si la petición es GET, simplemente mostramos el HTML
    return render_template('registro.html')


@auth_bp.route('/inicio_sesion', methods=['GET', 'POST'])
def inicio_sesion():
    """
    Maneja el inicio de sesión de los usuarios.
    """

    # Si el usuario ya está autenticado, lo mandamos a la app directamente
    if current_user.is_authenticated:
        flash("Ya has iniciado sesión.", "success")
        return redirect(url_for('pag_principal.inicio'))

    if request.method == 'POST':
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')

        # Usamos el repositorio para verificar las credenciales
        usuario = UsuarioRepository.verificar_credenciales(correo, contrasena)

        if usuario:
            # FLASK-LOGIN: Le pasamos el objeto entero y él gestiona la cookie de forma segura
            login_user(usuario)

            flash(f"¡Bienvenido, {usuario.correo}!", "success")
            # Lo mandamos a la pagina inicial
            return redirect(url_for('pag_principal.inicio'))
        else:
            flash("Correo o contraseña incorrectos.", "error")
            return redirect(url_for('auth.inicio_sesion'))

    # Si solo es GET
    return render_template('inicio_sesion.html')


@auth_bp.route('/cerrar_sesion')
@login_required
def cerrar_sesion():
    """Cierra la sesión del usuario actual."""

    # FLASK-LOGIN: Borra la sesión de este usuario específicamente
    logout_user()

    flash('Has cerrado la sesión exitosamente', 'success')
    return redirect(url_for('auth.inicio_sesion'))
