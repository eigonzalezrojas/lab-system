from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from src.models import Machine
from src import db

machine_bp = Blueprint('machine', __name__)


@machine_bp.route('/maquinas')
@login_required
def maquinas():
    maquinas = Machine.query.all()
    return render_template('admin_dashboard.html', section='maquinas', maquinas=maquinas)


@machine_bp.route('/crear_maquina', methods=['POST'])
@login_required
def crear_maquina():
    name = request.form['name']

    new_machine = Machine(name=name)
    db.session.add(new_machine)
    db.session.commit()

    flash('Máquina creada exitosamente.', 'success')
    return redirect(url_for('machine.maquinas'))


@machine_bp.route('/editar_maquina', methods=['POST'])
@login_required
def editar_maquina():
    id = request.form['id']
    machine = Machine.query.get(id)
    if machine:
        machine.name = request.form['name']
        db.session.commit()
        flash('Máquina actualizada exitosamente.', 'success')
    else:
        flash('Máquina no encontrada.', 'danger')
    return redirect(url_for('machine.maquinas'))


@machine_bp.route('/eliminar_maquina/<int:id>', methods=['DELETE'])
@login_required
def eliminar_maquina(id):
    machine = Machine.query.get(id)
    if machine:
        db.session.delete(machine)
        db.session.commit()
        return jsonify(success=True)
    else:
        return jsonify(success=False)
