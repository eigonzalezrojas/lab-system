from src.models.project import Project
from src import db


def get_all_projects():
    """Obtiene todos los proyectos de la base de datos."""
    return Project.query.all()


def create_project(name, fondo):
    """Crea un nuevo proyecto en la base de datos."""
    proyecto = Project(name=name, fondo=fondo)
    db.session.add(proyecto)
    db.session.commit()


def update_project(proyecto_id, name, fondo):
    """Actualiza los detalles de un proyecto existente."""
    proyecto = Project.query.get(proyecto_id)
    if proyecto:
        proyecto.name = name
        proyecto.fondo = fondo
        db.session.commit()
        return True
    return False


def delete_project(proyecto_id):
    """Elimina un proyecto de la base de datos por su ID."""
    proyecto = Project.query.get(proyecto_id)
    if proyecto:
        db.session.delete(proyecto)
        db.session.commit()
        return True
    return False


def get_project_by_id(project_id):
    return Project.query.get(project_id)