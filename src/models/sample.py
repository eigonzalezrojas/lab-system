from src import db

class Sample(db.Model):
    __tablename__ = 'samples'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    mg = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Sample {self.name}>'