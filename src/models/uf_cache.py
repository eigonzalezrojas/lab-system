from src import db
from datetime import datetime, date


class UFCache(db.Model):
    """Modelo para almacenar el valor de la UF en cache."""
    __tablename__ = 'uf_cache'
    __table_args__ = {'extend_existing': True}

    fecha = db.Column(db.Date, primary_key=True, nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<UFCache fecha={self.fecha} valor={self.valor}>'
