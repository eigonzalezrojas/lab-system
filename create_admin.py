import os
from app import app, db
from app.models import User, Role
from dotenv import load_dotenv

load_dotenv()

with app.app_context():
    # Verificar si el rol de administrador existe
    admin_role = Role.query.filter_by(name='administrador').first()
    if not admin_role:
        print("El rol 'administrador' no existe. Por favor, crea los roles primero.")
        exit()

    # Verificar si el usuario administrador ya existe
    admin_user = User.query.filter_by(email=os.getenv('ADMIN_EMAIL')).first()
    if not admin_user:
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
        print("Usuario administrador creado con éxito.")
    else:
        print("El usuario administrador ya existe.")
