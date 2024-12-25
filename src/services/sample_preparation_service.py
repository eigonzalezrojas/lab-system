from src.models import SamplePreparation
from src import db


def get_all_sample_preparations():
    """Obtiene todas las preparaciones de muestras de la base de datos."""
    return SamplePreparation.query.all()


def create_sample_preparation(name):
    """Crea una nueva preparación de muestra en la base de datos."""
    new_sample_preparation = SamplePreparation(name=name)
    db.session.add(new_sample_preparation)
    db.session.commit()


def update_sample_preparation(sample_preparation_id, name):
    """Actualiza los detalles de una preparación de muestra existente."""
    sample_preparation = SamplePreparation.query.get(sample_preparation_id)
    if sample_preparation:
        sample_preparation.name = name
        db.session.commit()
        return True
    return False


def delete_sample_preparation(sample_preparation_id):
    """Elimina una preparación de muestra de la base de datos por su ID."""
    sample_preparation = SamplePreparation.query.get(sample_preparation_id)
    if sample_preparation:
        db.session.delete(sample_preparation)
        db.session.commit()
        return True
    return False
