from werkzeug.security import generate_password_hash, check_password_hash
from src import db
from flask_login import UserMixin

class UserAccount(UserMixin, db.Model):
    __tablename__ = 'user_accounts'
    __table_args__ = {'extend_existing': True}
    rut = db.Column(db.String(12), primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('user_roles.id'), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role.name == 'administrador'

    def get_id(self):
        return self.rut

    def __repr__(self):
        return f'<UserAccount {self.email}>'