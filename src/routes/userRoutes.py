from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from src.services.user_service import get_all_users, get_all_roles, create_user, update_user, delete_user
from src.services.email_service import send_email
from src.models.userAccount import UserType

user_bp = Blueprint('user', __name__)


@user_bp.route('/usuarios')
@login_required
def usuarios():
    usuarios = get_all_users()
    roles = get_all_roles()
    return render_template('admin_dashboard.html', section='usuarios', usuarios=usuarios, roles=roles)


@user_bp.route('/crear_usuario', methods=['POST'])
@login_required
def crear_usuario():
    form_data = request.form.to_dict()
    form_data['type'] = UserType(form_data['type'])
    success, result = create_user(form_data)

    if success:
        subject = "Bienvenido al sistema del laboratorio IQRN"
        body = (
            "¡Bienvenido al sistema del laboratorio del IQRN!\n\n"
            "Nos complace darle acceso a nuestra plataforma. A continuación, encontrará su contraseña temporal, "
            "la cual deberá utilizar para iniciar sesión por primera vez. Por favor, recuerde cambiarla una vez que haya ingresado al sistema.\n\n"
            f"Su contraseña temporal es: {result}\n\n"
            "Si tiene alguna pregunta o necesita ayuda, no dude en ponerse en contacto con nuestro equipo de soporte.\n\n"
            "Atentamente,\n"
            "El equipo del laboratorio IQRN"
        )
        send_email(subject, request.form['email'], body)
        flash('Usuario creado exitosamente y contraseña enviada por correo.', 'success')
    else:
        flash(result, 'danger')

    return redirect(url_for('user.usuarios'))


@user_bp.route('/editar_usuario', methods=['POST'])
@login_required
def editar_usuario():
    try:
        form_data = request.form.to_dict()

        if 'type' in form_data:
            user_type = form_data['type'].upper()
            if user_type in UserType.__members__:
                form_data['type'] = UserType[user_type]
            else:
                flash('Tipo de usuario no válido.', 'danger')
                return redirect(url_for('user.usuarios'))

        if update_user(form_data):
            flash('Usuario actualizado exitosamente.', 'success')
        else:
            flash('Error al actualizar el usuario.', 'danger')
    except Exception as e:
        flash('Error al procesar la solicitud.', 'danger')

    return redirect(url_for('user.usuarios'))


@user_bp.route('/eliminar_usuario/<rut>', methods=['DELETE'])
@login_required
def eliminar_usuario(rut):
    if delete_user(rut):
        flash('Usuario eliminado exitosamente.', 'success')
        return jsonify(success=True)
    else:
        flash('Usuario no encontrado.', 'danger')
        return jsonify(success=False)
