from src import db

class Sample(db.Model):
    __tablename__ = 'samples'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    precio_interno = db.Column(db.Float, nullable=False, default=0.0)
    precio_externo = db.Column(db.Float, nullable=False, default=0.0)
    miligramos = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<Sample {self.name}>'