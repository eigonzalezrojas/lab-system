import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from dotenv import load_dotenv
from src import create_app, db
from src.models.userRole import UserRole

load_dotenv()

app = create_app()

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
