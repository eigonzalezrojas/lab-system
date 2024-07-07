import os
from app import app, db
from app.models import Role, User
from dotenv import load_dotenv

load_dotenv()

with app.app_context():
    db.create_all()

    # Crear roles
    admin_role = Role(name='administrador')
    operator_role = Role(name='operador')

    db.session.add(admin_role)
    db.session.add(operator_role)
    db.session.commit()

    # Crear usuario administrador utilizando variables de entorno
    admin_user = User(
        first_name=os.getenv('ADMIN_FIRST_NAME'),
        last_name=os.getenv('ADMIN_LAST_NAME'),
        rut=os.getenv('ADMIN_RUT'),
        email=os.getenv('ADMIN_EMAIL'),
        phone=os.getenv('ADMIN_PHONE'),
        role_id=admin_role.id
    )
    admin_user.set_password(os.getenv('ADMIN_PASSWORD'))

    db.session.add(admin_user)
    db.session.commit()
