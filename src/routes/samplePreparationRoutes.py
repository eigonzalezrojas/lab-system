from flask import Blueprint, request, redirect, url_for, render_template, flash
from src import db
from src.models import SamplePreparation
from flask_login import login_required

sample_preparation_bp = Blueprint('sample_preparation', __name__)

@sample_preparation_bp.route('/sample_preparations', methods=['GET'])
@login_required
def sample_preparations():
    sample_preparations = SamplePreparation.query.all()
    return render_template('admin_dashboard.html', section='sample_preparations', sample_preparations=sample_preparations)

@sample_preparation_bp.route('/crear_sample_preparation', methods=['POST'])
@login_required
def crear_sample_preparation():
    name = request.form.get('name')
    new_sample_preparation = SamplePreparation(name=name)
    db.session.add(new_sample_preparation)
    db.session.commit()
    flash('Sample Preparation creada con éxito', 'success')
    return redirect(url_for('sample_preparation.sample_preparations'))

@sample_preparation_bp.route('/editar_sample_preparation', methods=['POST'])
@login_required
def editar_sample_preparation():
    sample_preparation_id = request.form.get('id')
    sample_preparation = SamplePreparation.query.get(sample_preparation_id)
    sample_preparation.name = request.form.get('name')
    db.session.commit()
    flash('Sample Preparation actualizada con éxito', 'success')
    return redirect(url_for('sample_preparation.sample_preparations'))

@sample_preparation_bp.route('/eliminar_sample_preparation/<int:id>', methods=['DELETE'])
@login_required
def eliminar_sample_preparation(id):
    sample_preparation = SamplePreparation.query.get(id)
    db.session.delete(sample_preparation)
    db.session.commit()
    return {'success': True}
