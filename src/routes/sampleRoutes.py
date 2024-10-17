from flask import Blueprint, request, redirect, url_for, render_template, flash
from src.services.sample_service import get_all_samples, create_sample, update_sample, delete_sample
from flask_login import login_required

sample_bp = Blueprint('sample', __name__)


@sample_bp.route('/muestras', methods=['GET'])
@login_required
def muestras():
    samples = get_all_samples()  # Usar el servicio para obtener todas las muestras
    return render_template('admin_dashboard.html', section='samples', samples=samples)


@sample_bp.route('/crear_muestra', methods=['POST'])
@login_required
def crear_muestra():
    name = request.form.get('name')
    price = request.form.get('price')

    try:
        price = float(price)
    except ValueError:
        flash('El precio debe ser un número.', 'danger')
        return redirect(url_for('sample.muestras'))

    create_sample(name, price)  # Usar el servicio para crear una nueva muestra
    flash('Muestra creada con éxito', 'success')
    return redirect(url_for('sample.muestras'))


@sample_bp.route('/editar_muestra', methods=['POST'])
@login_required
def editar_muestra():
    sample_id = request.form.get('id')
    name = request.form.get('name')
    price = request.form.get('price')

    success, message = update_sample(sample_id, name, price)  # Usar el servicio para actualizar la muestra
    if success:
        flash('Muestra actualizada con éxito', 'success')
    else:
        flash(message, 'danger')

    return redirect(url_for('sample.muestras'))


@sample_bp.route('/eliminar_muestra/<int:id>', methods=['DELETE'])
@login_required
def eliminar_muestra(id):
    if delete_sample(id):  # Usar el servicio para eliminar la muestra
        return {'success': True}
    else:
        return {'success': False}
