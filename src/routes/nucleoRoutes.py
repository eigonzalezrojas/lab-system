from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required
from src.services.nucleo_service import get_all_nucleos, create_nucleo, update_nucleo, delete_nucleo

nucleo_bp = Blueprint('nucleo', __name__)


@nucleo_bp.route('/nucleos')
@login_required
def nucleos():
    nucleos = get_all_nucleos()  # Usar el servicio para obtener todos los núcleos
    return render_template('admin_dashboard.html', section='nucleos', nucleos=nucleos)


@nucleo_bp.route('/crear_nucleo', methods=['POST'])
@login_required
def crear_nucleo():
    nombre = request.form.get('nombre')
    precio = request.form.get('precio')

    create_nucleo(nombre, precio)  # Usar el servicio para crear un nuevo núcleo

    flash('Núcleo creado con éxito.', 'success')
    return redirect(url_for('nucleo.nucleos'))


@nucleo_bp.route('/editar_nucleo', methods=['POST'])
@login_required
def editar_nucleo():
    nucleo_id = request.form.get('id')
    nombre = request.form.get('nombre')
    precio = request.form.get('precio')

    if update_nucleo(nucleo_id, nombre, precio):  # Usar el servicio para actualizar el núcleo
        flash('Núcleo actualizado con éxito.', 'success')
    else:
        flash('Núcleo no encontrado.', 'danger')

    return redirect(url_for('nucleo.nucleos'))


@nucleo_bp.route('/eliminar_nucleo/<int:nucleo_id>', methods=['DELETE'])
@login_required
def eliminar_nucleo(nucleo_id):
    if delete_nucleo(nucleo_id):  # Usar el servicio para eliminar el núcleo
        return jsonify(success=True)
    else:
        return jsonify(success=False), 404
