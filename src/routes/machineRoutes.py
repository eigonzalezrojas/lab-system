from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from src.services.machine_service import get_all_machines, create_machine, update_machine, delete_machine

machine_bp = Blueprint('machine', __name__)


@machine_bp.route('/maquinas')
@login_required
def maquinas():
    maquinas = get_all_machines()  # Usar el servicio para obtener todas las máquinas
    return render_template('admin_dashboard.html', section='maquinas', maquinas=maquinas)


@machine_bp.route('/crear_maquina', methods=['POST'])
@login_required
def crear_maquina():
    name = request.form['name']
    create_machine(name)  # Usar el servicio para crear una nueva máquina

    flash('Máquina creada exitosamente.', 'success')
    return redirect(url_for('machine.maquinas'))


@machine_bp.route('/editar_maquina', methods=['POST'])
@login_required
def editar_maquina():
    machine_id = request.form['id']
    name = request.form['name']

    if update_machine(machine_id, name):  # Usar el servicio para actualizar la máquina
        flash('Máquina actualizada exitosamente.', 'success')
    else:
        flash('Máquina no encontrada.', 'danger')

    return redirect(url_for('machine.maquinas'))


@machine_bp.route('/eliminar_maquina/<int:id>', methods=['DELETE'])
@login_required
def eliminar_maquina(id):
    if delete_machine(id):  # Usar el servicio para eliminar la máquina
        return jsonify(success=True)
    else:
        return jsonify(success=False)
