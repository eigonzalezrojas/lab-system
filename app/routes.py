from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, login_required, logout_user
from app import app, db
from app.models import UserAccount
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
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid RUT or Password', 'danger')
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
                flash('A temporary password has been sent to your email.', 'success')
            else:
                flash('There was an error sending the email. Please try again later.', 'danger')
        else:
            flash('RUT not found in the system.', 'danger')
    return render_template('forgot_password.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin_dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
