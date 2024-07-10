import os
from app import app, db
from app.models import UserAccount, UserRole
from dotenv import load_dotenv

load_dotenv()

with app.app_context():
    try:
        # Verificar si el rol de operador existe
        operator_role = UserRole.query.filter_by(name='operador').first()
        if not operator_role:
            print("El rol 'operador' no existe. Por favor, ejecuta primero create_roles.py.")
            exit()

        # Verificar si el usuario administrador ya existe
        if not UserAccount.query.filter_by(email=os.getenv('OP_EMAIL')).first():
            operator_user = UserAccount(
                first_name=os.getenv('OP_FIRST_NAME'),
                last_name=os.getenv('OP_LAST_NAME'),
                rut=os.getenv('OP_RUT'),
                email=os.getenv('OP_EMAIL'),
                phone=os.getenv('OP_PHONE'),
                role_id=operator_role.id
            )
            operator_user.set_password(os.getenv('OP_PASSWORD'))
            db.session.add(operator_user)
            db.session.commit()
            print("Usuario operador creado con éxito.")
        else:
            print("El usuario operador ya existe.")
    except Exception as e:
        db.session.rollback()
        print(f"Ha ocurrido un error: {e}")
