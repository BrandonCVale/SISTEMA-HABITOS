from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from typing import Optional

from flask_login import LoginManager

# Inicializamos el login manager
login_manager = LoginManager()

# Inicializamos ORM (herramienta que conecta a Python con la BD)
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Llave secreta necesaria para usar sesiones y la función flash()
    app.config['SECRET_KEY'] = 'sistema_habitos_76Fu-39+'

    # Configuración de la base de datos SQLite (se guardará en un archivo local)
    # URI de SQLITE
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habitos.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Activa el modo "echo" para ver el SQL real en la consola
    app.config['SQLALCHEMY_ECHO'] = True

    # Conectamos la base de datos con nuestra aplicación
    db.init_app(app)

    # Configuramos el guardia de Login Manager
    login_manager.init_app(app)
    # Le decimos donde debe mandar a los usuarios que intenten entrar sin permiso
    login_manager.login_view = 'auth.inicio_sesion'
    login_manager.login_message = 'Por favor inicia sesión para acceder.'
    login_manager.login_message_category = 'error'

    # Le enseñamos al guardia de Login Manager como buscar a un usuario con su ID guardado en la cookie
    from app.models.usuario import Usuario
    @login_manager.user_loader
    def load_user(user_id: str) -> Optional[Usuario]:
        """
        Recupera un usuario de la base de datos usando el ID almacenado en la cookie de sesión.
        Args:
            user_id (str): El ID del usuario extraído de la cookie (Flask-Login siempre lo envía como texto).
        Returns:
            Optional[Usuario]: El objeto Usuario si es encontrado, o None si no existe en la base de datos.
        """
        # Convertimos el ID de texto a número entero para buscarlo por su llave primaria
        return db.session.get(Usuario, int(user_id))

    # Registro de Blueprints
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    from app.routes.pagina_principal import pag_principal_bp
    app.register_blueprint(pag_principal_bp)
    from app.routes.habito import habito_bp
    app.register_blueprint(habito_bp)

    # Ruta principal que redirige automáticamente al inicio de sesión
    @app.route('/')
    def index():
        return redirect(url_for('auth.inicio_sesion'))

    return app
