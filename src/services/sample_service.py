from src.models import Sample
from src import db


def get_all_samples():
    """Obtiene todas las muestras de la base de datos."""
    return Sample.query.all()


def create_sample(name, price):
    """Crea una nueva muestra en la base de datos."""
    new_sample = Sample(name=name, price=price)
    db.session.add(new_sample)
    db.session.commit()


def update_sample(sample_id, name, price):
    """Actualiza los detalles de una muestra existente."""
    sample = Sample.query.get(sample_id)
    if sample:
        sample.name = name
        try:
            sample.price = float(price)
            db.session.commit()
            return True
        except ValueError:
            return False, "El precio debe ser un número."
    return False, "Muestra no encontrada."


def delete_sample(sample_id):
    """Elimina una muestra de la base de datos por su ID."""
    sample = Sample.query.get(sample_id)
    if sample:
        db.session.delete(sample)
        db.session.commit()
        return True
    return False
