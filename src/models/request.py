from src import db
from datetime import datetime


class Request(db.Model):
    __tablename__ = 'requests'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_rut = db.Column(db.String(12), db.ForeignKey('user_accounts.rut'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    solvent_id = db.Column(db.Integer, db.ForeignKey('solvents.id'), nullable=False)
    sample_preparation_id = db.Column(db.Integer, db.ForeignKey('sample_preparation.id'),nullable=False)
    sample_id = db.Column(db.Integer, db.ForeignKey('samples.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    request_name = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float, nullable=False)

    user = db.relationship('UserAccount', backref=db.backref('requests', lazy=True))
    project = db.relationship('Project', backref=db.backref('requests', lazy=True))
    solvent = db.relationship('Solvent', backref=db.backref('requests', lazy=True))
    sample_preparation = db.relationship('SamplePreparation', backref=db.backref('requests', lazy=True))
    sample = db.relationship('Sample', backref=db.backref('requests', lazy=True))

    def __repr__(self):
        return f'<Request {self.request_name}>'
