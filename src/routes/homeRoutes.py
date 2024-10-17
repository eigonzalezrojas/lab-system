from flask import Blueprint, render_template
from flask_login import login_required, current_user
from src.services.home_services import get_statistics, get_operator_statistics
from src.models import Request

home_bp = Blueprint('home', __name__)


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