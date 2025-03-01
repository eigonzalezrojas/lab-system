import os
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from werkzeug.security import generate_password_hash, check_password_hash
from src.models import UserAccount
from src import db
from flask_login import login_user, logout_user, current_user


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
        server = smtplib.SMTP(smtp_server, int(smtp_port))
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def authenticate_user(rut, password):
    user = UserAccount.query.filter_by(rut=rut).first()
    if user and user.check_password(password):
        login_user(user)
        return user
    else:
        return None


def generate_temporary_password(user):
    temporary_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    user.temporary_password = temporary_password
    db.session.commit()
    return True


def update_password(current_password, new_password, confirm_password):
    if not check_password_hash(current_user.password_hash, current_password):
        return False, "La contraseña actual es incorrecta"
    elif new_password != confirm_password:
        return False, "La nueva contraseña y la confirmación no coinciden"
    else:
        current_user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        logout_user()
        return True, "Contraseña actualizada con éxito"
