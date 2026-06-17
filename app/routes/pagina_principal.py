"""
Módulo de Rutas de la Pagina Principal.

Maneja la pantalla principal del usuario una vez que ha iniciado sesión.
Aquí se mostrará el catálogo de hábitos (RF-03).
"""

import calendar
from flask import Blueprint, render_template
from datetime import date
from flask_login import login_required, current_user

# Traer los habitos y poder mostrarlos en el html de la página principal
from app.repositories.habito_repository import HabitoRepository

# Creamos el blueprint de la pagina principal
pag_principal_bp = Blueprint('pag_principal', __name__, url_prefix='/pagina_principal')


@pag_principal_bp.route('/inicio', methods=['GET'])
@login_required
def inicio():
    """
    Muestra el panel principal.
    Esta ruta está PROTEGIDA: requiere haber iniciado sesión.
    Si alguien sin sesión intenta entrar, Flask-Login lo manda al login automáticamente.
    """

    # Traer los habitos del repositorio
    habitos_usuario = HabitoRepository.obtener_habitos_por_usuario(current_user.id)

    hoy = date.today()
    
    # Mapeo para traducir el número de Python (0=Lunes) a nuestras letras
    mapa_dias = {0: 'L', 1: 'M', 2: 'X', 3: 'J', 4: 'V', 5: 'S', 6: 'D'}
    letra_hoy = mapa_dias[hoy.weekday()]
    
    habitos_hoy = []
    
    for habito in habitos_usuario:
        habito.completado_hoy = any(registro.fecha == hoy for registro in habito.registros)
        # Filtramos: Solo lo agregamos a la lista si está activo y toca hacerlo hoy
        if habito.activo and letra_hoy in habito.dias_semana:
            habitos_hoy.append(habito)

    # ================= LOGICA DEL CALENDARIO =================
    # 1. Averiguamos cuántos días tiene el mes y en qué día de la semana empieza (0=Lunes, 6=Domingo)
    _, num_dias = calendar.monthrange(hoy.year, hoy.month)
    dia_semana_inicio = date(hoy.year, hoy.month, 1).weekday()
    
    # 2. Consultamos nuestro repositorio
    dias_completados = HabitoRepository.obtener_dias_activos_mes(current_user.id, hoy.year, hoy.month)
    
    # 3. Obtenemos el nombre del mes en español
    nombres_meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    mes_actual = nombres_meses[hoy.month - 1]

    # ================= LÓGICA DE LOS KPIs =================
    # Contamos cuántos hábitos DE HOY se han completado
    habitos_completados_hoy = sum(1 for h in habitos_hoy if h.completado_hoy)
    
    # Obtenemos la racha más alta entre todos sus hábitos (si no tiene, devuelve 0)
    racha_actual = max([h.racha_actual for h in habitos_usuario] + [0])
    mejor_racha = max([h.mejor_racha for h in habitos_usuario] + [0])

    return render_template("pagina_principal.html",
                           usuario=current_user,
                           habitos=habitos_hoy,
                           mes_actual=mes_actual,
                           num_dias=num_dias,
                           dia_semana_inicio=dia_semana_inicio,
                           dias_completados=dias_completados,
                           habitos_completados_hoy=habitos_completados_hoy,
                           racha_actual=racha_actual,
                           mejor_racha=mejor_racha)
