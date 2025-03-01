from src import db
from datetime import datetime


class Request(db.Model):
    __tablename__ = 'requests'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(128), nullable=False)
    user_rut = db.Column(db.String(12), nullable=False)
    project_name = db.Column(db.String(64), nullable=False)
    machine_name = db.Column(db.String(64), nullable=False)
    solvent_name = db.Column(db.String(64), nullable=False)
    sample_preparation_name = db.Column(db.String(64), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    recovery = db.Column(db.String(3), nullable=False)
    request_name = db.Column(db.String(64), nullable=False)
    estado = db.Column(db.String(20), nullable=False, default='Pendiente')
    sample_ids = db.Column(db.String(256), nullable=False)
    nucleo_ids = db.Column(db.String(256), nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    c13_miligramos = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<Request {self.project_name} - Estado: {self.estado}>'

