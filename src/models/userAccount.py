from werkzeug.security import generate_password_hash, check_password_hash
from src import db
from flask_login import UserMixin
from enum import Enum
class UserType(Enum):
    INTERNAL = "interno"
    EXTERNAL = "externo"

class UserAccount(UserMixin, db.Model):
    __tablename__ = 'user_accounts'
    __table_args__ = {'extend_existing': True}

    rut = db.Column(db.String(12), primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('user_roles.id'), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    temporary_password = db.Column(db.String(255), nullable=True)
    type = db.Column(db.Enum(UserType), nullable=False, default=UserType.INTERNAL)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """ Verifica la contraseña ingresada con la almacenada en `password_hash` o `temporary_password`. """
        # Verificamos la contraseña normal
        if check_password_hash(self.password_hash, password):
            return True

        # Verificamos la contraseña temporal
        if self.temporary_password and check_password_hash(self.temporary_password, password):
            return True

        return False

    def is_admin(self):
        return self.role.name == 'administrador'

    def get_id(self):
        return self.rut

    def __repr__(self):
        return f'<UserAccount {self.email}>'