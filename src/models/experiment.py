from src import db

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