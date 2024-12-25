from src import db

class SamplePreparation(db.Model):
    __tablename__ = 'sample_preparation'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f'<Sample Preparation {self.name}>'
