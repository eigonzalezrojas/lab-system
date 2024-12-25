from src.models import Sample
from src import db


def get_all_samples():
    return Sample.query.all()


def create_sample(name, precio_interno, precio_externo):
    sample = Sample(name=name, precio_interno=precio_interno, precio_externo=precio_externo)
    db.session.add(sample)
    db.session.commit()


def update_sample(sample_id, name, precio_interno, precio_externo):
    sample = Sample.query.get(sample_id)
    if sample:
        sample.name = name
        sample.precio_interno = precio_interno
        sample.precio_externo = precio_externo
        db.session.commit()
        return True, "Muestra actualizada correctamente"
    else:
        return False, "Muestra no encontrada"


def delete_sample(sample_id):    
    sample = Sample.query.get(sample_id)
    if sample:
        db.session.delete(sample)
        db.session.commit()
        return True
    return False
