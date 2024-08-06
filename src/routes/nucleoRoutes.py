from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required
from src import db
from src.models import Nucleo

nucleo_bp = Blueprint('nucleo', __name__)

@nucleo_bp.route('/nucleos')
@login_required
def nucleos():
    nucleos = Nucleo.query.all()
    return render_template('admin_dashboard.html', section='nucleos', nucleos=nucleos)

@nucleo_bp.route('/crear_nucleo', methods=['POST'])
@login_required
def crear_nucleo():
    nombre = request.form.get('nombre')
    precio = request.form.get('precio')

    nuevo_nucleo = Nucleo(nombre=nombre, precio=precio)
    db.session.add(nuevo_nucleo)
    db.session.commit()

    flash('Núcleo creado con éxito.', 'success')
    return redirect(url_for('nucleo.nucleos'))

@nucleo_bp.route('/editar_nucleo', methods=['POST'])
@login_required
def editar_nucleo():
    nucleo_id = request.form.get('id')
    nombre = request.form.get('nombre')
    precio = request.form.get('precio')

    nucleo = Nucleo.query.get(nucleo_id)
    if nucleo:
        nucleo.nombre = nombre
        nucleo.precio = precio
        db.session.commit()
        flash('Núcleo actualizado con éxito.', 'success')
    else:
        flash('Núcleo no encontrado.', 'danger')

    return redirect(url_for('nucleo.nucleos'))

@nucleo_bp.route('/eliminar_nucleo/<int:nucleo_id>', methods=['DELETE'])
@login_required
def eliminar_nucleo(nucleo_id):
    nucleo = Nucleo.query.get(nucleo_id)
    if nucleo:
        db.session.delete(nucleo)
        db.session.commit()
        return jsonify(success=True)
    else:
        return jsonify(success=False), 404
