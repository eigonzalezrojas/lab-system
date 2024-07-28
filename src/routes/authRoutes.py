from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from src.models import UserAccount
from src import db
import os
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

auth_bp = Blueprint('auth', __name__)

def send_email(subject, recipient, body):
    sender_email = os.getenv('EMAIL_USER')
    sender_password = os.getenv('EMAIL_PASS')
    smtp_server = os.getenv('EMAIL_HOST')
    smtp_port = os.getenv('EMAIL_PORT')

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        rut = request.form['rut']
        password = request.form['password']
        user = UserAccount.query.filter_by(rut=rut).first()
        if user and user.check_password(password):
            login_user(user)
            if user.is_admin():
                return redirect(url_for('main.admin_dashboard'))
            else:
                return redirect(url_for('main.operador_dashboard'))
        else:
            flash('Rut y/o contraseña inválida', 'danger')
    return render_template('login.html')

@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        rut = request.form['rut']
        user = UserAccount.query.filter_by(rut=rut).first()
        if user:
            temporary_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            user.set_password(temporary_password)
            db.session.commit()
            subject = "Contraseña temporal"
            body = f"Su contraseña temporal es: {temporary_password}"
            if send_email(subject, user.email, body):
                flash('Una contraseña fue enviada a su correo registrado', 'success')
            else:
                flash('Hubo un error en el envío del correo', 'danger')
        else:
            flash('El Rut ingresado no está registrado', 'danger')
    return render_template('forgot_password.html')


@auth_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not check_password_hash(current_user.password_hash, current_password):
            flash('La contraseña actual es incorrecta', 'danger')
        elif new_password != confirm_password:
            flash('La nueva contraseña y la confirmación no coinciden', 'danger')
        else:
            current_user.password_hash = generate_password_hash(new_password)
            db.session.commit()
            flash('Contraseña actualizada con éxito', 'success')
            return redirect(url_for('home.home'))

    return render_template('change_password.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
