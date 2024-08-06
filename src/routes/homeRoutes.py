from flask import Blueprint, render_template
from flask_login import login_required
from src.models import UserAccount, Project, Machine, Solvent, Sample, SamplePreparation, Request
from src import db

home_bp = Blueprint('home', __name__)

def get_statistics():
    total_usuarios = UserAccount.query.count()
    total_proyectos = Project.query.count()
    total_maquinas = Machine.query.count()
    total_solventes = Solvent.query.count()
    total_muestras = Sample.query.count()
    total_preparaciones = SamplePreparation.query.count()
    return {
        'total_usuarios': total_usuarios,
        'total_proyectos': total_proyectos,
        'total_maquinas': total_maquinas,
        'total_solventes': total_solventes,
        'total_muestras': total_muestras,
        'total_preparaciones': total_preparaciones,
    }

def get_operator_statistics():
    total_solicitudes = Request.query.count()
    total_proyectos = Project.query.count()

    # Calcular la suma de los fondos restantes
    suma_fondos = db.session.query(db.func.sum(Project.fondo)).scalar()
    suma_fondos = round(float(suma_fondos or 0), 2)

    # Obtener todas las solicitudes para mostrar en la tabla
    solicitudes = Request.query.all()

    return {
        'total_solicitudes': total_solicitudes,
        'total_proyectos': total_proyectos,
        'suma_fondos': suma_fondos,
        'solicitudes': solicitudes
    }


@home_bp.route('/home')
@login_required
def home():
    stats = get_statistics()
    return render_template('admin_dashboard.html', section='home', **stats)

@home_bp.route('/home_operator')
@login_required
def home_operator():
    stats = get_operator_statistics()
    return render_template('operador_dashboard.html', section='home', **stats)
