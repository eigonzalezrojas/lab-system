from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from src.services.auth_services import authenticate_user, generate_password_hash, update_password
from src.services.email_service import send_email
from src.models import UserAccount, UserType
import time, random, string
from src import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        rut = request.form['rut']
        password = request.form['password']
        user = authenticate_user(rut, password)

        if user:
            # Si el usuario usa una contraseña temporal, redirigir al cambio de contraseña
            if user.temporary_password and user.temporary_password == password:
                flash('Has ingresado con una contraseña temporal. Por favor, cámbiala.', 'warning')
                return redirect(url_for('auth.change_password'))

            # Iniciar sesión con una contraseña válida
            login_user(user)

            if user.is_admin():
                return redirect(url_for('home.home'))
            elif user.type == UserType.INTERNAL:
                return redirect(url_for('main.operador_interno_dashboard'))
            elif user.type == UserType.EXTERNAL:
                return redirect(url_for('main.operador_externo_dashboard'))

        flash('Rut y/o contraseña inválida', 'danger')

    return render_template('login.html')


@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        rut = request.form.get('rut')
        if not rut:
            flash('Debe ingresar un RUT.', 'danger')
            return redirect(url_for('auth.forgot_password'))

        user = UserAccount.query.filter_by(rut=rut).first()
        if user:
            temp_password = generate_temporary_password(user)

            if temp_password:
                subject = "Contraseña Temporal IQRN"
                body = f"""
                Estimado/a {user.first_name},

                Hemos recibido una solicitud para restablecer su contraseña. Para acceder a su cuenta, utilice la siguiente contraseña temporal:

                🔑 Contraseña temporal: {temp_password}

                Por favor, inicie sesión y cambie su contraseña lo antes posible para garantizar la seguridad de su cuenta.

                Si usted no solicitó este cambio, por favor ignore este mensaje.

                Atentamente,  
                El equipo de soporte de IQRN
                """

                if send_email(subject, user.email, body):
                    flash('Una contraseña fue enviada a su correo registrado', 'success')
                else:
                    flash('Hubo un error en el envío del correo.', 'danger')
            else:
                flash('No se pudo generar la contraseña temporal.', 'danger')
        else:
            flash('El RUT ingresado no está registrado.', 'danger')

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


def generate_temporary_password(user):
    """ Genera y hashea una contraseña temporal usando werkzeug.security """

    # Generamos una contraseña aleatoria de 10 caracteres
    temporary_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    if not temporary_password:
        return None

    # Hasheamos la contraseña antes de guardarla en la base de datos
    hashed_temp_password = generate_password_hash(temporary_password)

    # Guardamos la contraseña temporal hasheada en la base de datos
    user.temporary_password = hashed_temp_password
    db.session.commit()

    return temporary_password



def update_password(current_password, new_password, confirm_password):
    """ Actualiza la contraseña del usuario, verificando la contraseña actual """

    user = UserAccount.query.get_or_404(current_user.rut)

    # Verificar que la contraseña actual sea correcta (contraseña normal o temporal)
    if not user.check_password(current_password):
        return False, "La contraseña actual es incorrecta."

    # Verificar que la nueva contraseña y la confirmación coincidan
    if new_password != confirm_password:
        return False, "Las contraseñas no coinciden."

    # Guardar la nueva contraseña y eliminar la contraseña temporal
    user.set_password(new_password)
    user.temporary_password = None
    db.session.commit()

    return True, "Contraseña actualizada exitosamente."
