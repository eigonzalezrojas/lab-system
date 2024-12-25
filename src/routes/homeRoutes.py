from flask import Blueprint, render_template
from flask_login import login_required
from src.services.home_services import get_statistics
from src.services.solicitudes_service import obtener_valor_uf

home_bp = Blueprint('home', __name__)

@home_bp.route('/home')
@login_required
def home():
    stats = get_statistics()
    
    valor_uf = obtener_valor_uf()
    if valor_uf is None:
        valor_uf = "No disponible"
    else:
        valor_uf = f"{valor_uf:,.2f}"
    
    stats['valor_uf'] = valor_uf
    
    return render_template('admin_dashboard.html', section='home', **stats)