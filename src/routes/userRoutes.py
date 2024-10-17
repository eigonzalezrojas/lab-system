from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from src.services.user_service import get_all_users, get_all_roles, create_user, update_user, delete_user
from src.services.email_service import send_email

user_bp = Blueprint('user', __name__)


@user_bp.route('/usuarios')
@login_required
def usuarios():
    usuarios = get_all_users()  # Usar el servicio para obtener todos los usuarios
    roles = get_all_roles()  # Usar el servicio para obtener todos los roles
    return render_template('admin_dashboard.html', section='usuarios', usuarios=usuarios, roles=roles)


@user_bp.route('/crear_usuario', methods=['POST'])
@login_required
def crear_usuario():
    success, result = create_user(request.form)  # Usar el servicio para crear un nuevo usuario

    if success:
        subject = "Bienvenido al sistema"
        body = f"Su contraseña temporal es: {result}"
        send_email(subject, request.form['email'], body)  # Enviar el correo al nuevo usuario
        flash('Usuario creado exitosamente y contraseña enviada por correo.', 'success')
    else:
        flash(result, 'danger')

    return redirect(url_for('user.usuarios'))


@user_bp.route('/editar_usuario', methods=['POST'])
@login_required
def editar_usuario():
    if update_user(request.form):  # Usar el servicio para actualizar el usuario
        flash('Usuario actualizado exitosamente.', 'success')
    else:
        flash('Usuario no encontrado.', 'danger')
    return redirect(url_for('user.usuarios'))


@user_bp.route('/eliminar_usuario/<rut>', methods=['DELETE'])
@login_required
def eliminar_usuario(rut):
    if delete_user(rut):  # Usar el servicio para eliminar el usuario
        flash('Usuario eliminado exitosamente.', 'success')
        return jsonify(success=True)
    else:
        flash('Usuario no encontrado.', 'danger')
        return jsonify(success=False)