from src.models import Machine
from src import db


def get_all_machines():
    """Obtiene todas las máquinas de la base de datos."""
    return Machine.query.all()


def create_machine(name):
    """Crea una nueva máquina y la guarda en la base de datos."""
    new_machine = Machine(name=name)
    db.session.add(new_machine)
    db.session.commit()


def update_machine(machine_id, name):
    """Actualiza los detalles de una máquina existente."""
    machine = Machine.query.get(machine_id)
    if machine:
        machine.name = name
        db.session.commit()
        return True
    return False


def delete_machine(machine_id):
    """Elimina una máquina por su ID."""
    machine = Machine.query.get(machine_id)
    if machine:
        db.session.delete(machine)
        db.session.commit()
        return True
    return False


def get_machine_by_id(machine_id):
    return Machine.query.get(machine_id)