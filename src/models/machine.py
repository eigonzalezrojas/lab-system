from src import db

class Machine(db.Model):
    __tablename__ = 'machines'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f'<Machine {self.name}>'