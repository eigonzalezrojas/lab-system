from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, current_user, login_required, logout_user
from app import app, db
from app.models import UserAccount, UserRole
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()


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


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        rut = request.form['rut']
        password = request.form['password']
        user = UserAccount.query.filter_by(rut=rut).first()
        if user and user.check_password(password):
            login_user(user)
            if user.is_admin():
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('operador_dashboard'))
        else:
            flash('Rut y/o contraseña inválida', 'danger')
    return render_template('login.html')


@app.route('/forgot_password', methods=['GET', 'POST'])
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
                flash('Un contraseña fue enviada a su correo registrado', 'success')
            else:
                flash('Hubo un error en el envío del correo', 'danger')
        else:
            flash('El Rut ingresado no está registrado', 'danger')
    return render_template('forgot_password.html')


@app.route('/usuarios')
@login_required
def usuarios():
    usuarios = UserAccount.query.all()
    roles = UserRole.query.all()
    return render_template('admin_dashboard.html', section='usuarios', usuarios=usuarios, roles=roles)


@app.route('/crear_usuario', methods=['POST'])
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
        return redirect(url_for('usuarios'))

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
    return redirect(url_for('usuarios'))


@app.route('/editar_usuario', methods=['POST'])
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
    return redirect(url_for('usuarios'))


@app.route('/eliminar_usuario/<rut>', methods=['DELETE'])
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



@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    return render_template('admin_dashboard.html')


@app.route('/operador_dashboard')
@login_required
def operador_dashboard():
    return render_template('operador_dashboard.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
