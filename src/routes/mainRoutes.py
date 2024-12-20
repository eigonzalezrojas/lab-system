from flask import Blueprint, redirect, url_for
from flask_login import login_required

main_bp = Blueprint('main', __name__)


@main_bp.route('/admin_dashboard')
@login_required
def admin_dashboard():
    return redirect(url_for('home.home'))


@main_bp.route('/operador_dashboard')
@login_required
def operador_dashboard():
    return redirect(url_for('home.home_operator'))
