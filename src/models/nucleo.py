from src import db

class Nucleo(db.Model):
    __tablename__ = 'nucleos'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), nullable=False)
    precio = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Nucleo {self.nombre}>'
