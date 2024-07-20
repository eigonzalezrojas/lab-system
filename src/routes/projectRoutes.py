from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from src.models.project import Project
from src import db

project_bp = Blueprint('project', __name__)

@project_bp.route('/proyectos')
@login_required
def proyectos():
    proyectos = Project.query.all()
    return render_template('admin_dashboard.html', section='proyectos', proyectos=proyectos)

@project_bp.route('/crear_proyecto', methods=['POST'])
@login_required
def crear_proyecto():
    name = request.form['name']
    fondo = request.form['fondo']

    proyecto = Project(name=name, fondo=fondo)
    db.session.add(proyecto)
    db.session.commit()

    flash('Proyecto creado exitosamente.', 'success')
    return redirect(url_for('project.proyectos'))

@project_bp.route('/editar_proyecto', methods=['POST'])
@login_required
def editar_proyecto():
    proyecto_id = request.form['id']
    proyecto = Project.query.get(proyecto_id)
    if proyecto:
        proyecto.name = request.form['name']
        proyecto.fondo = request.form['fondo']
        db.session.commit()
        flash('Proyecto actualizado exitosamente.', 'success')
    else:
        flash('Proyecto no encontrado.', 'danger')
    return redirect(url_for('project.proyectos'))

@project_bp.route('/eliminar_proyecto/<int:id>', methods=['DELETE'])
@login_required
def eliminar_proyecto(id):
    proyecto = Project.query.get(id)
    if proyecto:
        db.session.delete(proyecto)
        db.session.commit()
        flash('Proyecto eliminado exitosamente.', 'success')
        return jsonify(success=True)
    else:
        flash('Proyecto no encontrado.', 'danger')
        return jsonify(success=False)
