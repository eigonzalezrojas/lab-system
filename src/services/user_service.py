from src.models import UserAccount, UserRole
from src import db
import random
import string


def get_all_users():
    """Obtiene todos los usuarios de la base de datos."""
    return UserAccount.query.all()


def get_all_roles():
    """Obtiene todos los roles de usuario de la base de datos."""
    return UserRole.query.all()


def create_user(data):
    """Crea un nuevo usuario con una contraseña temporal."""
    rut = data.get('rut')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone = data.get('phone')
    email = data.get('email')
    role_id = data.get('role_id')

    user = UserAccount.query.filter_by(rut=rut).first()
    if user:
        return False, 'El usuario con este RUT ya está registrado.'

    # Generar una contraseña temporal
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

    return True, temporary_password


def update_user(data):
    """Actualiza los datos de un usuario existente."""
    original_rut = data.get('original_rut')
    user = UserAccount.query.filter_by(rut=original_rut).first()

    if user:
        user.rut = data.get('rut')
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.phone = data.get('phone')
        user.email = data.get('email')
        user.role_id = data.get('role_id')
        db.session.commit()
        return True
    return False


def delete_user(rut):
    """Elimina un usuario de la base de datos."""
    user = UserAccount.query.filter_by(rut=rut).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False
