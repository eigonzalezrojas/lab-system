
from flask import Blueprint, render_template
from flask_login import login_required
from src.models import UserAccount, Project, Machine, Solvent, Sample, SamplePreparation

home_bp = Blueprint('home', __name__)

@home_bp.route('/home')
@login_required
def home():
    total_usuarios = UserAccount.query.count()
    total_proyectos = Project.query.count()
    total_maquinas = Machine.query.count()
    total_solventes = Solvent.query.count()
    total_muestras = Sample.query.count()
    total_preparaciones = SamplePreparation.query.count()

    return render_template('admin_dashboard.html',
                           section='home',
                           total_usuarios=total_usuarios,
                           total_proyectos=total_proyectos,
                           total_maquinas=total_maquinas,
                           total_solventes=total_solventes,
                           total_muestras=total_muestras,
                           total_preparaciones=total_preparaciones)
