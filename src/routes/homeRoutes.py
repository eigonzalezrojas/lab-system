from flask import Blueprint, render_template
from flask_login import login_required, current_user
from src.models import UserAccount, Project, Machine, Solvent, Sample, SamplePreparation, Request, Nucleo, Invoice
from src import db

home_bp = Blueprint('home', __name__)

def get_statistics():
    total_usuarios = UserAccount.query.count()
    total_proyectos = Project.query.count()
    total_maquinas = Machine.query.count()
    total_solventes = Solvent.query.count()
    total_muestras = Sample.query.count()
    total_preparaciones = SamplePreparation.query.count()
    total_nucleos = Nucleo.query.count()
    total_solicitudes = Request.query.count()

    return {
        'total_usuarios': total_usuarios,
        'total_proyectos': total_proyectos,
        'total_maquinas': total_maquinas,
        'total_solventes': total_solventes,
        'total_muestras': total_muestras,
        'total_preparaciones': total_preparaciones,
        'total_nucleos': total_nucleos,
        'total_solicitudes': total_solicitudes
    }

@home_bp.route('/home')
@login_required
def home():
    stats = get_statistics()
    return render_template('admin_dashboard.html', section='home', **stats)


@home_bp.route('/home_operator')
@login_required
def home_operator():
    # Filtrar las solicitudes asociadas al operador actual por su RUT
    solicitudes = Request.query.filter_by(user_rut=current_user.rut).all()

    # Pasar las solicitudes filtradas a la función get_operator_statistics
    stats = get_operator_statistics(solicitudes)

    return render_template('operador_dashboard.html', section='home', solicitudes=solicitudes, **stats)


def get_operator_statistics(solicitudes):
    total_solicitudes = len(solicitudes)
    total_proyectos = Project.query.count()

    # Calcular el total de facturas (sumando el costo total de las solicitudes)
    total_facturas = sum(solicitud.total_cost for solicitud in solicitudes)

    return {
        'total_solicitudes': total_solicitudes,
        'total_proyectos': total_proyectos,
        'total_facturas': total_facturas,
    }


