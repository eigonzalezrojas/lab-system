from src.models import Nucleo
from src import db


def get_all_nucleos():
    return Nucleo.query.all()


def create_nucleo(nombre, precio_interno, precio_externo):
    nucleo = Nucleo(nombre=nombre, precio_interno=precio_interno, precio_externo=precio_externo)
    db.session.add(nucleo)
    db.session.commit()


def update_nucleo(nucleo_id, nombre, precio_interno, precio_externo):
    nucleo = Nucleo.query.get(nucleo_id)
    if nucleo:
        nucleo.nombre = nombre
        nucleo.precio_interno = precio_interno
        nucleo.precio_externo = precio_externo
        db.session.commit()
        return True, "Núcleo actualizado correctamente"
    else:
        return False, "Núcleo no encontrado"


def delete_nucleo(nucleo_id):
    nucleo = Nucleo.query.get(nucleo_id)
    if nucleo:
        db.session.delete(nucleo)
        db.session.commit()
        return True
    return False
