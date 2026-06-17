"""
Módulo de Rutas de Hábitos.

Maneja las operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
para la entidad Hábito.
"""
from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_required, current_user

from app.repositories.habito_repository import HabitoRepository

# Creamos el Blueprint para las rutas de hábitos
habito_bp = Blueprint('habitos', __name__, url_prefix='/habitos')


@habito_bp.route('/mis_habitos', methods=['GET'])
@login_required
def mis_habitos():
    """Muestra la pantalla de gestión de todos los hábitos."""

    # Usaremos request.args.get, que sirve para leer lo que viene escrito arriba en la URL.
    # Atrapamos el filtro de la URL (ej. ?estado=inactivos). Si está vacía, ponemos 'activos' por defecto
    estado_filtro = request.args.get('estado', 'activos')

    # Solicitar los habitos del usuario aplicando el filtro
    habitos_usuario = HabitoRepository.obtener_habitos_por_usuario(current_user.id, estado=estado_filtro)

    # Servimos la interfaz habitos.html
    return render_template("habitos.html",
                           usuario=current_user,
                           habitos=habitos_usuario,
                           estado_actual=estado_filtro)


@habito_bp.route('/crear', methods=['POST'])
@login_required
def crear():
    """Procesa los datos del formulario para crear un nuevo hábito."""

    # Extraemos el nombre, la descripción y los días del formulario HTML
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    dias_lista = request.form.getlist('dias')  # nos devuelve una lista de Python

    # convertimos la lista de 'dias_lista' porque
    # la BD no conoce el tipo lista, solo string
    dias_texto = ",".join(dias_lista) if dias_lista else ""

    if not nombre or not dias_lista:
        flash("El nombre del hábito y los dias de la semana son obligatorios.", "error")
        return redirect(url_for('pag_principal.inicio'))

    # Usamos el repositorio para crear el hábito
    HabitoRepository.crear_habito(nombre=nombre,
                                  usuario_id=current_user.id,
                                  descripcion=descripcion,
                                  dias_semana=dias_texto)

    flash("¡Hábito creado con éxito!", "success")
    return redirect(url_for('pag_principal.inicio'))


@habito_bp.route('/editar/<int:id_habito>', methods=['GET', 'POST'])
@login_required
def editar(id_habito):
    """Edita la información de un habito creado previamente"""

    # Buscamos el hábito actual por su id para cargar los datos en el html de editar
    habito = HabitoRepository.obtener_habito_por_id(id_habito)
    # Validación breve
    if not habito or habito.usuario_id != current_user.id:
        flash("Habito no encontrado o  no tienes permiso para editarlo", "error")
        return redirect(url_for('habitos.mis_habitos'))

    if request.method == 'POST':
        # Extraemos los datos del formulario
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        dias_lista = request.form.getlist('dias')
        activo = request.form.get('activo') == 'on'  # Si el checkbox esta marcado llego como on

        dias_texto = ",".join(dias_lista) if dias_lista else ""

        HabitoRepository.editar_habito(
            habito_id=id_habito,
            nombre=nombre,
            descripcion=descripcion,
            dias_semana=dias_texto,
            activo=activo
        )
        flash("Hábito actualizado", "success")
        return redirect(url_for('habitos.mis_habitos'))
    else:
        # Si es GET
        return render_template("editar_habito.html",
                               usuario=current_user,
                               habito=habito)


@habito_bp.route('/visualizar_progreso/<int:id_habito>', methods=['GET'])
@login_required
def visualizar_progreso(id_habito):
    """Permite visualizar el gráfico de avance de un hábito en específico"""

    # Buscamos el habito
    habito = HabitoRepository.obtener_habito_por_id(id_habito)
    if not habito or habito.usuario_id != current_user.id:
        flash("Hábito no encontrado o no tienes permiso para ver el progreso", "error")
        return redirect(url_for('habitos.mis_habitos'))

    # Llamamos al servicio para calcular y dibujar la grafica
    from app.services.estadisticas_grafica import EstadisticasService
    grafica_html = EstadisticasService.generar_grafica_ultimos_dias(habito.registros)

    # Servimos la interfaz enviando el HTML de la grafica
    return render_template('visualizar_progreso.html',
                           usuario=current_user,
                           habito=habito,
                           grafica_html=grafica_html)


@habito_bp.route('/eliminar/<int:id_habito>', methods=['POST'])
@login_required
def eliminar(id_habito):
    """Permite eliminar un hábito"""

    # 1. Buscamos el hábito primero para saber si existe y de quién es
    habito = HabitoRepository.obtener_habito_por_id(id_habito)

    # 2. Validación de seguridad (El candado)
    if not habito or habito.usuario_id != current_user.id:
        flash("Hábito no encontrado o no tienes permiso para eliminarlo.", "error")
        return redirect(url_for('habitos.mis_habitos'))

    # 3. Si pasó la validación, procedemos a eliminarlo
    HabitoRepository.eliminar_habito(id_habito)

    flash("Hábito eliminado con éxito", "success")
    return redirect(url_for('habitos.mis_habitos'))


@habito_bp.route('/completar/<int:id_habito>', methods=['POST'])
@login_required
def completar(id_habito):
    """Marca un hábito como completado o desmarcado en el día actual."""
    habito = HabitoRepository.obtener_habito_por_id(id_habito)

    if not habito or habito.usuario_id != current_user.id:
        flash("No tienes permiso para modificar este hábito.", "error")
        return redirect(url_for('pag_principal.inicio'))

    estado = HabitoRepository.marcar_completado_hoy(id_habito)

    if estado:
        flash(f"¡Genial! Has completado '{habito.nombre}' hoy. 🔥", "success")
    else:
        flash(f"Has desmarcado '{habito.nombre}'.", "success")

    return redirect(url_for('pag_principal.inicio'))
