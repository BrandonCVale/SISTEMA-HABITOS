"""
Punto de entrada principal del Sistema de Hábitos.

Este script inicializa la aplicación web, configura la base de datos
y arranca el servidor local de desarrollo.
"""

from app import create_app, db
# IMPORTANTE: Aunque no usemos 'Usuario' y 'Habito' directamente aquí,
# debemos importarlos para que SQLAlchemy sepa qué tablas debe crear.
from app.models import Usuario, Habito

# Creamos la instancia de la aplicación usando nuestra "Fábrica"
app = create_app()

# Abrimos un "contexto de aplicación" para interactuar con la configuración
with app.app_context():
    db.create_all()
    print("Base de datos y tablas verificadas/creadas con éxito.")

if __name__ == '__main__':
    # Arrancamos el servidor en modo depuración (debug=True)
    # Esto recargará el servidor automáticamente si detecta cambios en el código.
    app.run(debug=True, host='0.0.0.0')
