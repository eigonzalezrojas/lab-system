from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_required, current_user
from src.models import Project, Machine, Solvent, SamplePreparation, Sample, Request
from src import db
from fpdf import FPDF

solicitudes_bp = Blueprint('solicitudes', __name__)

@solicitudes_bp.route('/solicitudes')
@login_required
def solicitudes():
    projects = Project.query.all()
    machines = Machine.query.all()
    return render_template('operador_dashboard.html', section='solicitudes', projects=projects, machines=machines)

@solicitudes_bp.route('/nueva_solicitud', methods=['POST'])
@login_required
def nueva_solicitud():
    project_id = request.form.get('project_id')
    machine_id = request.form.get('machine_id')

    project = Project.query.get(project_id)
    machine = Machine.query.get(machine_id)
    solvents = Solvent.query.all()
    sample_preparations = SamplePreparation.query.all()
    samples = Sample.query.all()

    if not project or not machine:
        flash('Proyecto o Máquina no encontrados.', 'danger')
        return redirect(url_for('solicitudes.solicitudes'))

    return render_template(
        'operador_dashboard.html',
        section='nueva_solicitud',
        project=project,
        machine=machine,
        solvents=solvents,
        sample_preparations=sample_preparations,
        samples=samples
    )

@solicitudes_bp.route('/agregar_solicitud', methods=['POST'])
@login_required
def agregar_solicitud():
    sample_name = request.form.get('sample_name')
    solvent_id = request.form.get('solvent_id')
    sample_preparation_id = request.form.get('sample_preparation_id')
    recovery = request.form.get('recovery')
    sample_ids = request.form.getlist('sample_ids')
    project_id = request.form.get('project_id')
    machine_id = request.form.get('machine_id')

    new_request = Request(
        user_rut=current_user.rut,
        project_id=project_id,
        solvent_id=solvent_id,
        sample_preparation_id=sample_preparation_id,
        sample_id=sample_ids[0],  # Asegúrate de manejar esto según tus necesidades
        request_name=sample_name,
        price=0  # Ajusta esto según sea necesario
    )

    db.session.add(new_request)
    db.session.commit()

    flash('Solicitud agregada con éxito', 'success')
    return redirect(url_for('solicitudes.solicitudes'))

@solicitudes_bp.route('/descargar/<int:solicitud_id>', methods=['GET'])
@login_required
def descargar(solicitud_id):
    solicitud = Request.query.get_or_404(solicitud_id)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Agregar información de la solicitud al PDF
    pdf.cell(200, 10, txt=f"Solicitud: {solicitud.request_name}", ln=True)
    pdf.cell(200, 10, txt=f"Usuario: {solicitud.user_rut}", ln=True)
    pdf.cell(200, 10, txt=f"Proyecto: {solicitud.project.name}", ln=True)
    pdf.cell(200, 10, txt=f"Solvente: {solicitud.solvent.name}", ln=True)
    pdf.cell(200, 10, txt=f"Preparación de Muestra: {solicitud.sample_preparation.name}", ln=True)
    pdf.cell(200, 10, txt=f"Muestra: {solicitud.sample.name}", ln=True)
    pdf.cell(200, 10, txt=f"Fecha: {solicitud.fecha.strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(200, 10, txt=f"Precio: {solicitud.price}", ln=True)

    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=solicitud_{solicitud_id}.pdf'
    return response
