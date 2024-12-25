from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from src.services.project_service import get_all_projects, create_project, update_project, delete_project

project_bp = Blueprint('project', __name__)


@project_bp.route('/proyectos')
@login_required
def proyectos():
    proyectos = get_all_projects()  # Usar el servicio para obtener todos los proyectos
    return render_template('admin_dashboard.html', section='proyectos', proyectos=proyectos)


@project_bp.route('/crear_proyecto', methods=['POST'])
@login_required
def crear_proyecto():
    name = request.form['name']
    fondo = request.form['fondo']

    create_project(name, fondo)  # Usar el servicio para crear un nuevo proyecto

    flash('Proyecto creado exitosamente.', 'success')
    return redirect(url_for('project.proyectos'))


@project_bp.route('/editar_proyecto', methods=['POST'])
@login_required
def editar_proyecto():
    proyecto_id = request.form['id']
    name = request.form['name']
    fondo = request.form['fondo']

    if update_project(proyecto_id, name, fondo):  # Usar el servicio para actualizar el proyecto
        flash('Proyecto actualizado exitosamente.', 'success')
    else:
        flash('Proyecto no encontrado.', 'danger')

    return redirect(url_for('project.proyectos'))


@project_bp.route('/eliminar_proyecto/<int:id>', methods=['DELETE'])
@login_required
def eliminar_proyecto(id):
    if delete_project(id):  # Usar el servicio para eliminar el proyecto
        flash('Proyecto eliminado exitosamente.', 'success')
        return jsonify(success=True)
    else:
        flash('Proyecto no encontrado.', 'danger')
        return jsonify(success=False)
