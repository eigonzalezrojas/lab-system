from flask import Blueprint, request, redirect, url_for, render_template, flash
from src import db
from src.models import Solvent
from flask_login import login_required

solvent_bp = Blueprint('solvent', __name__)

@solvent_bp.route('/solventes', methods=['GET'])
@login_required
def solventes():
    solvents = Solvent.query.all()
    return render_template('admin_dashboard.html', section='solventes', solvents=solvents)

@solvent_bp.route('/crear_solvente', methods=['POST'])
@login_required
def crear_solvente():
    name = request.form.get('name')
    new_solvent = Solvent(name=name)
    db.session.add(new_solvent)
    db.session.commit()
    flash('Solvente creado con éxito', 'success')
    return redirect(url_for('solvent.solventes'))

@solvent_bp.route('/editar_solvente', methods=['POST'])
@login_required
def editar_solvente():
    solvent_id = request.form.get('id')
    solvent = Solvent.query.get(solvent_id)
    solvent.name = request.form.get('name')
    db.session.commit()
    flash('Solvente actualizado con éxito', 'success')
    return redirect(url_for('solvent.solventes'))

@solvent_bp.route('/eliminar_solvente/<int:id>', methods=['DELETE'])
@login_required
def eliminar_solvente(id):
    solvent = Solvent.query.get(id)
    db.session.delete(solvent)
    db.session.commit()
    return {'success': True}
