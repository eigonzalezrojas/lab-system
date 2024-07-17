from src import db

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