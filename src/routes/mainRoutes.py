from flask import Blueprint, render_template
from flask_login import login_required, current_user
from src.services.solicitudes_service import get_all_solicitudes_with_details, obtener_valor_uf  # Agregada importación
from src.services.project_service import get_all_projects
from src.services.machine_service import get_all_machines
from src.services.sample_service import get_all_samples
from src.services.nucleo_service import get_all_nucleos
from src.services.solvent_service import get_all_solvents
from src.services.sample_preparation_service import get_all_sample_preparations


main_bp = Blueprint('main', __name__)

@main_bp.route('/operador_interno_dashboard')
@login_required
def operador_interno_dashboard():
    solicitudes = get_all_solicitudes_with_details(current_user.rut)
    projects = get_all_projects()
    machines = get_all_machines()
    samples = get_all_samples()
    nucleos = get_all_nucleos()
    solvents = get_all_solvents()
    sample_preparations = get_all_sample_preparations()

    total_solicitudes = len(solicitudes)
    total_proyectos = len(projects)

    # Obtener el valor de la UF
    valor_uf = obtener_valor_uf()
    if valor_uf is None:
        valor_uf = "No disponible"
    else:
        valor_uf = f"{valor_uf:,.2f}"

    user_type = 'internal'

    return render_template('operador_dashboard_interno.html',
                           section='home',
                           solicitudes=solicitudes,
                           projects=projects,
                           machines=machines,
                           samples=samples,
                           nucleos=nucleos,
                           solvents=solvents,
                           sample_preparations=sample_preparations,
                           total_solicitudes=total_solicitudes,
                           total_proyectos=total_proyectos,
                           user_type=user_type,
                           valor_uf=valor_uf)

@main_bp.route('/operador_externo_dashboard')
@login_required
def operador_externo_dashboard():
    solicitudes = get_all_solicitudes_with_details(current_user.rut)
    projects = get_all_projects()
    machines = get_all_machines()
    samples = get_all_samples()
    nucleos = get_all_nucleos()
    solvents = get_all_solvents()
    sample_preparations = get_all_sample_preparations()

    total_solicitudes = len(solicitudes)
    total_proyectos = len(projects)

    # Obtener el valor de la UF
    valor_uf = obtener_valor_uf()
    if valor_uf is None:
        valor_uf = "No disponible"
    else:
        valor_uf = f"{valor_uf:,.2f}"

    user_type = 'external'

    return render_template('operador_dashboard_externo.html',
                           section='home',
                           solicitudes=solicitudes,
                           projects=projects,
                           machines=machines,
                           samples=samples,
                           nucleos=nucleos,
                           solvents=solvents,
                           sample_preparations=sample_preparations,
                           total_solicitudes=total_solicitudes,
                           total_proyectos=total_proyectos,
                           user_type=user_type,
                           valor_uf=valor_uf)