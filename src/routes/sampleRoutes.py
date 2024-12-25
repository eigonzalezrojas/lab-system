from flask import Blueprint, request, redirect, url_for, render_template, flash
from src.services.sample_service import get_all_samples, create_sample, update_sample, delete_sample
from flask_login import login_required

sample_bp = Blueprint('sample', __name__)


@sample_bp.route('/muestras', methods=['GET'])
@login_required
def muestras():
    samples = get_all_samples()
    return render_template('admin_dashboard.html', section='samples', samples=samples)


@sample_bp.route('/crear_muestra', methods=['POST'])
@login_required
def crear_muestra():
    name = request.form.get('name')
    precio_interno = request.form.get('precio_interno')
    precio_externo = request.form.get('precio_externo')

    try:
        precio_interno = float(precio_interno)
        precio_externo = float(precio_externo)
    except ValueError:
        flash('Los precios deben ser números.', 'danger')
        return redirect(url_for('sample.muestras'))

    create_sample(name, precio_interno, precio_externo)
    flash('Muestra creada con éxito', 'success')
    return redirect(url_for('sample.muestras'))


@sample_bp.route('/editar_muestra', methods=['POST'])
@login_required
def editar_muestra():
    sample_id = request.form.get('id')
    name = request.form.get('name')
    precio_interno = request.form.get('precio_interno')
    precio_externo = request.form.get('precio_externo')

    success, message = update_sample(sample_id, name, precio_interno, precio_externo)
    if success:
        flash('Muestra actualizada con éxito', 'success')
    else:
        flash(message, 'danger')

    return redirect(url_for('sample.muestras'))


@sample_bp.route('/eliminar_muestra/<int:id>', methods=['DELETE'])
@login_required
def eliminar_muestra(id):
    if delete_sample(id):
        return {'success': True}
    else:
        return {'success': False}
