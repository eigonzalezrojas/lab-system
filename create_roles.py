import os
from app import app, db
from app.models import UserRole
from dotenv import load_dotenv

load_dotenv()

with app.app_context():
    try:
        db.create_all()

        if not UserRole.query.filter_by(name='administrador').first():
            admin_role = UserRole(name='administrador')
            db.session.add(admin_role)
            print("Rol 'administrador' creado.")
        else:
            print("El rol 'administrador' ya existe.")

        if not UserRole.query.filter_by(name='operador').first():
            operator_role = UserRole(name='operador')
            db.session.add(operator_role)
            print("Rol 'operador' creado.")
        else:
            print("El rol 'operador' ya existe.")

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Ha ocurrido un error: {e}")
