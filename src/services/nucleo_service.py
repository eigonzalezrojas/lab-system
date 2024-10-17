from src.models import Nucleo
from src import db


def get_all_nucleos():
    """Obtiene todos los núcleos de la base de datos."""
    return Nucleo.query.all()


def create_nucleo(nombre, precio):
    """Crea un nuevo núcleo en la base de datos."""
    nuevo_nucleo = Nucleo(nombre=nombre, precio=precio)
    db.session.add(nuevo_nucleo)
    db.session.commit()


def update_nucleo(nucleo_id, nombre, precio):
    """Actualiza los detalles de un núcleo existente."""
    nucleo = Nucleo.query.get(nucleo_id)
    if nucleo:
        nucleo.nombre = nombre
        nucleo.precio = precio
        db.session.commit()
        return True
    return False


def delete_nucleo(nucleo_id):
    """Elimina un núcleo de la base de datos por su ID."""
    nucleo = Nucleo.query.get(nucleo_id)
    if nucleo:
        db.session.delete(nucleo)
        db.session.commit()
        return True
    return False
