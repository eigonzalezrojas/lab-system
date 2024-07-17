from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from src.models import UserAccount, UserRole
from src import db
import random
import string
from .authRoutes import send_email

user_bp = Blueprint('user', __name__)

@user_bp.route('/usuarios')
@login_required
def usuarios():
    usuarios = UserAccount.query.all()
    roles = UserRole.query.all()
    return render_template('admin_dashboard.html', section='usuarios', usuarios=usuarios, roles=roles)

@user_bp.route('/crear_usuario', methods=['POST'])
@login_required
def crear_usuario():
    rut = request.form['rut']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    phone = request.form['phone']
    email = request.form['email']
    role_id = request.form['role_id']

    user = UserAccount.query.filter_by(rut=rut).first()
    if user:
        flash('El usuario con este RUT ya está registrado.', 'danger')
        return redirect(url_for('user.usuarios'))

    temporary_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    new_user = UserAccount(
        rut=rut,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        email=email,
        role_id=role_id
    )
    new_user.set_password(temporary_password)
    db.session.add(new_user)
    db.session.commit()

    subject = "Bienvenido al sistema"
    body = f"Su contraseña temporal es: {temporary_password}"
    send_email(subject, email, body)

    flash('Usuario creado exitosamente y contraseña enviada por correo.', 'success')
    return redirect(url_for('user.usuarios'))

@user_bp.route('/editar_usuario', methods=['POST'])
@login_required
def editar_usuario():
    original_rut = request.form['original_rut']
    user = UserAccount.query.filter_by(rut=original_rut).first()
    if user:
        user.rut = request.form['rut']
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.phone = request.form['phone']
        user.email = request.form['email']
        user.role_id = request.form['role_id']

        db.session.commit()
        flash('Usuario actualizado exitosamente.', 'success')
    else:
        flash('Usuario no encontrado.', 'danger')
    return redirect(url_for('user.usuarios'))

@user_bp.route('/eliminar_usuario/<rut>', methods=['DELETE'])
@login_required
def eliminar_usuario(rut):
    user = UserAccount.query.filter_by(rut=rut).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('Usuario eliminado exitosamente.', 'success')
        return jsonify(success=True)
    else:
        flash('Usuario no encontrado.', 'danger')
        return jsonify(success=False)
