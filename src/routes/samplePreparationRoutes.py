from flask import Blueprint, request, redirect, url_for, render_template, flash
from src.services.sample_preparation_service import get_all_sample_preparations, create_sample_preparation, update_sample_preparation, delete_sample_preparation
from flask_login import login_required

sample_preparation_bp = Blueprint('sample_preparation', __name__)


@sample_preparation_bp.route('/sample_preparations', methods=['GET'])
@login_required
def sample_preparations():
    sample_preparations = get_all_sample_preparations()  # Usar el servicio para obtener todas las preparaciones de muestras
    return render_template('admin_dashboard.html', section='sample_preparations', sample_preparations=sample_preparations)


@sample_preparation_bp.route('/crear_sample_preparation', methods=['POST'])
@login_required
def crear_sample_preparation():
    name = request.form.get('name')
    create_sample_preparation(name)  # Usar el servicio para crear una nueva preparación de muestra

    flash('Sample Preparation creada con éxito', 'success')
    return redirect(url_for('sample_preparation.sample_preparations'))


@sample_preparation_bp.route('/editar_sample_preparation', methods=['POST'])
@login_required
def editar_sample_preparation():
    sample_preparation_id = request.form.get('id')
    name = request.form.get('name')

    if update_sample_preparation(sample_preparation_id, name):  # Usar el servicio para actualizar la preparación de muestra
        flash('Sample Preparation actualizada con éxito', 'success')
    else:
        flash('Sample Preparation no encontrada', 'danger')

    return redirect(url_for('sample_preparation.sample_preparations'))


@sample_preparation_bp.route('/eliminar_preparacion/<int:id>', methods=['DELETE'])
@login_required
def eliminar_sample_preparation(id):
    if delete_sample_preparation(id):  # Usar el servicio para eliminar la preparación de muestra
        return {'success': True}
    else:
        return {'success': False}
