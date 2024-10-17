from flask import Blueprint, request, redirect, url_for, render_template, flash
from src.services.solvent_service import get_all_solvents, create_solvent, update_solvent, delete_solvent
from flask_login import login_required

solvent_bp = Blueprint('solvent', __name__)


@solvent_bp.route('/solventes', methods=['GET'])
@login_required
def solventes():
    solvents = get_all_solvents()  # Usar el servicio para obtener todos los solventes
    return render_template('admin_dashboard.html', section='solventes', solvents=solvents)


@solvent_bp.route('/crear_solvente', methods=['POST'])
@login_required
def crear_solvente():
    name = request.form.get('name')
    create_solvent(name)  # Usar el servicio para crear un nuevo solvente
    flash('Solvente creado con éxito', 'success')
    return redirect(url_for('solvent.solventes'))


@solvent_bp.route('/editar_solvente', methods=['POST'])
@login_required
def editar_solvente():
    solvent_id = request.form.get('id')
    name = request.form.get('name')

    if update_solvent(solvent_id, name):  # Usar el servicio para actualizar el solvente
        flash('Solvente actualizado con éxito', 'success')
    else:
        flash('Solvente no encontrado', 'danger')

    return redirect(url_for('solvent.solventes'))


@solvent_bp.route('/eliminar_solvente/<int:id>', methods=['DELETE'])
@login_required
def eliminar_solvente(id):
    if delete_solvent(id):  # Usar el servicio para eliminar el solvente
        return {'success': True}
    else:
        return {'success': False}
