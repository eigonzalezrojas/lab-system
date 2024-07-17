from flask import Blueprint, render_template
from flask_login import login_required, current_user
from src.models import UserAccount, UserRole

main_bp = Blueprint('main', __name__)

@main_bp.route('/admin_dashboard')
@login_required
def admin_dashboard():
    return render_template('admin_dashboard.html')

@main_bp.route('/operador_dashboard')
@login_required
def operador_dashboard():
    return render_template('operador_dashboard.html')
