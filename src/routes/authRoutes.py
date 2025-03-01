from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from src.services.auth_services import authenticate_user, generate_temporary_password, update_password
from src.services.email_service import send_email
from src.models import UserAccount, UserType
import time

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        rut = request.form['rut']
        password = request.form['password']
        user = authenticate_user(rut, password)
        if user:
            if user.is_admin():
                return redirect(url_for('home.home'))
            else:
                if user.type == UserType.INTERNAL:
                    return redirect(url_for('main.operador_interno_dashboard'))
                elif user.type == UserType.EXTERNAL:
                    return redirect(url_for('main.operador_externo_dashboard'))
                else:
                    flash('Rut y/o contraseña inválida', 'danger')
                return render_template('login.html')
        else:
            flash('Rut y/o contraseña inválida', 'danger')
    return render_template('login.html')


@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        rut = request.form['rut']
        user = UserAccount.query.filter_by(rut=rut).first()
        if user:
            if generate_temporary_password(user):
                subject = "Contraseña Temporal IQRN"
                body = f"""
                Estimado/a {user.first_name},

                Hemos recibido una solicitud para restablecer su contraseña. Para acceder a su cuenta, utilice la siguiente contraseña temporal:

                🔑 Contraseña temporal: **{user.temporary_password}**

                Por favor, inicie sesión y cambie su contraseña lo antes posible para garantizar la seguridad de su cuenta.

                Si usted no solicitó este cambio, por favor ignore este mensaje.

                Atentamente,  
                El equipo de soporte de IQRN
                """

                if send_email(subject, user.email, body):
                    flash('Una contraseña fue enviada a su correo registrado', 'success')
                else:
                    flash('Hubo un error en el envío del correo', 'danger')
            else:
                flash('Hubo un error al generar la contraseña temporal', 'danger')
        else:
            flash('El Rut ingresado no está registrado', 'danger')
        time.sleep(1)
        return redirect(url_for('auth.login'))
    return render_template('forgot_password.html')



@auth_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        success, message = update_password(current_password, new_password, confirm_password)
        if success:
            flash(message, 'success')
            time.sleep(1)
            return redirect(url_for('auth.login'))
        else:
            flash(message, 'danger')

    return render_template('change_password.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))