from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db

class UserRole(db.Model):
    __tablename__ = 'user_roles'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    users = db.relationship('UserAccount', backref='role', lazy=True)

    def __repr__(self):
        return f'<UserRole {self.name}>'


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

class Project(db.Model):
    __tablename__ = 'projects'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f'<Project {self.name}>'


class Machine(db.Model):
    __tablename__ = 'machines'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f'<Machine {self.name}>'


class Solvent(db.Model):
    __tablename__ = 'solvents'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f'<Solvent {self.name}>'


class Preparation(db.Model):
    __tablename__ = 'preparations'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f'<Preparation {self.name}>'


class Sample(db.Model):
    __tablename__ = 'samples'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    mg = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Sample {self.name}>'


class Request(db.Model):
    __tablename__ = 'requests'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(64), nullable=False)
    value = db.Column(db.Float, nullable=False)

    project = db.relationship('Project', backref=db.backref('requests', lazy=True))
    machine = db.relationship('Machine', backref=db.backref('requests', lazy=True))

    def __repr__(self):
        return f'<Request {self.id}>'


class Experiment(db.Model):
    __tablename__ = 'experiments'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    solvent_id = db.Column(db.Integer, db.ForeignKey('solvents.id'), nullable=False)
    preparation_id = db.Column(db.Integer, db.ForeignKey('preparations.id'), nullable=False)
    sample_id = db.Column(db.Integer, db.ForeignKey('samples.id'), nullable=False)
    observation = db.Column(db.Text, nullable=True)
    sample_recovery = db.Column(db.Float, nullable=False)

    solvent = db.relationship('Solvent', backref=db.backref('experiments', lazy=True))
    preparation = db.relationship('Preparation', backref=db.backref('experiments', lazy=True))
    sample = db.relationship('Sample', backref=db.backref('experiments', lazy=True))

    def __repr__(self):
        return f'<Experiment {self.name}>'


class Invoice(db.Model):
    __tablename__ = 'invoices'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_first_name = db.Column(db.String(64), nullable=False)
    user_last_name = db.Column(db.String(64), nullable=False)
    user_rut = db.Column(db.String(12), db.ForeignKey('user_accounts.rut'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    user = db.relationship('UserAccount', backref=db.backref('invoices', lazy=True))

    def __repr__(self):
        return f'<Invoice {self.id}>'
