import os
from app import app, db
from app.models import UserAccount, UserRole
from dotenv import load_dotenv

load_dotenv()

with app.app_context():
    try:
        # Verificar si el rol de administrador existe
        admin_role = UserRole.query.filter_by(name='administrador').first()
        if not admin_role:
            print("El rol 'administrador' no existe. Por favor, ejecuta primero create_roles.py.")
            exit()

        # Verificar si el usuario administrador ya existe
        if not UserAccount.query.filter_by(email=os.getenv('ADMIN_EMAIL')).first():
            admin_user = UserAccount(
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
    except Exception as e:
        db.session.rollback()
        print(f"Ha ocurrido un error: {e}")
