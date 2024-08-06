from flask import Blueprint, request, redirect, url_for, render_template, flash
from src import db
from src.models import Sample
from flask_login import login_required

sample_bp = Blueprint('sample', __name__)

@sample_bp.route('/muestras', methods=['GET'])
@login_required
def muestras():
    samples = Sample.query.all()
    return render_template('admin_dashboard.html', section='samples', samples=samples)

@sample_bp.route('/crear_muestra', methods=['POST'])
@login_required
def crear_muestra():
    name = request.form.get('name')
    price = request.form.get('price')  # Obtener el precio del formulario

    try:
        price = float(price)
    except ValueError:
        flash('El precio debe ser un número.', 'danger')
        return redirect(url_for('sample.muestras'))

    new_sample = Sample(name=name, price=price)
    db.session.add(new_sample)
    db.session.commit()
    flash('Muestra creada con éxito', 'success')
    return redirect(url_for('sample.muestras'))

@sample_bp.route('/editar_muestra', methods=['POST'])
@login_required
def editar_muestra():
    sample_id = request.form.get('id')
    sample = Sample.query.get(sample_id)

    if not sample:
        flash('Muestra no encontrada.', 'danger')
        return redirect(url_for('sample.muestras'))

    sample.name = request.form.get('name')
    price = request.form.get('price')  # Obtener el precio del formulario

    try:
        sample.price = float(price)
    except ValueError:
        flash('El precio debe ser un número.', 'danger')
        return redirect(url_for('sample.muestras'))

    db.session.commit()
    flash('Muestra actualizada con éxito', 'success')
    return redirect(url_for('sample.muestras'))

@sample_bp.route('/eliminar_muestra/<int:id>', methods=['DELETE'])
@login_required
def eliminar_muestra(id):
    sample = Sample.query.get(id)
    db.session.delete(sample)
    db.session.commit()
    return {'success': True}
