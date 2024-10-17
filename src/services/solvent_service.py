from src.models import Solvent
from src import db


def get_all_solvents():
    """Obtiene todos los solventes de la base de datos."""
    return Solvent.query.all()


def create_solvent(name):
    """Crea un nuevo solvente en la base de datos."""
    new_solvent = Solvent(name=name)
    db.session.add(new_solvent)
    db.session.commit()


def update_solvent(solvent_id, name):
    """Actualiza los detalles de un solvente existente."""
    solvent = Solvent.query.get(solvent_id)
    if solvent:
        solvent.name = name
        db.session.commit()
        return True
    return False


def delete_solvent(solvent_id):
    """Elimina un solvente de la base de datos por su ID."""
    solvent = Solvent.query.get(solvent_id)
    if solvent:
        db.session.delete(solvent)
        db.session.commit()
        return True
    return False
