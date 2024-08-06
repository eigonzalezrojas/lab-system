from flask import Blueprint, render_template, request, make_response, redirect, url_for, flash
from flask_login import login_required, current_user
from src.models import Project, Machine, Solvent, SamplePreparation, Sample, Request, Nucleo
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
    nucleos = Nucleo.query.all()  # Obtener todos los núcleos

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
        samples=samples,
        nucleos=nucleos  # Pasar núcleos a la plantilla
    )

@solicitudes_bp.route('/agregar_solicitud', methods=['POST'])
@login_required
def agregar_solicitud():
    sample_name = request.form.get('sample_name')
    solvent_id = request.form.get('solvent_id')
    sample_preparation_id = request.form.get('sample_preparation_id')
    recovery = request.form.get('recovery')
    sample_ids = request.form.getlist('sample_ids')
    nucleo_ids = request.form.getlist('nucleo_ids')

    # Obtener y procesar muestras
    samples = Sample.query.filter(Sample.id.in_(sample_ids)).all()
    # Obtener y procesar núcleos
    nucleos = Nucleo.query.filter(Nucleo.id.in_(nucleo_ids)).all()

    # Calcular el precio total
    total_price = sum(sample.price for sample in samples) + sum(nucleo.precio for nucleo in nucleos)

    # Verificar el proyecto
    project_id = request.form.get('project_id')
    project = Project.query.get(project_id)

    if project is None:
        flash('Proyecto no encontrado.', 'danger')
        return redirect(url_for('solicitudes.solicitudes'))

    # Verificar si el total de la solicitud excede el fondo del proyecto
    if total_price > project.fondo:
        flash('El monto de la solicitud excede el fondo del proyecto.', 'danger')
        return redirect(url_for('solicitudes.solicitudes'))

    # Restar el total de la solicitud del fondo del proyecto
    project.fondo -= total_price
    db.session.commit()

    # Crear una nueva solicitud
    nueva_solicitud = Request(
        user_name=current_user.first_name + " " + current_user.last_name,
        user_rut=current_user.rut,
        project_name=project.name,
        solvent_name=Solvent.query.get(solvent_id).name,
        sample_preparation_name=SamplePreparation.query.get(sample_preparation_id).name,
        sample_name=sample_name,
        request_name=sample_name,
        price=total_price,  # Guardar el precio total
        estado='Pendiente'
    )

    db.session.add(nueva_solicitud)
    db.session.commit()

    flash('Solicitud agregada con éxito', 'success')
    return redirect(url_for('solicitudes.solicitudes'))


@solicitudes_bp.route('/descargar/<int:solicitud_id>', methods=['GET'])
@login_required
def descargar(solicitud_id):
    solicitud = Request.query.get_or_404(solicitud_id)

    # Crear PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Nombre del Usuario: {solicitud.user_name}", ln=True)
    pdf.cell(200, 10, txt=f"RUT del Usuario: {solicitud.user_rut}", ln=True)
    pdf.cell(200, 10, txt=f"Nombre de la Solicitud: {solicitud.request_name}", ln=True)
    pdf.cell(200, 10, txt=f"Proyecto: {solicitud.project_name}", ln=True)
    pdf.cell(200, 10, txt=f"Solvente: {solicitud.solvent_name}", ln=True)
    pdf.cell(200, 10, txt=f"Preparación de Muestra: {solicitud.sample_preparation_name}", ln=True)
    pdf.cell(200, 10, txt=f"Muestra: {solicitud.sample_name}", ln=True)
    pdf.cell(200, 10, txt=f"Fecha: {solicitud.fecha.strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(200, 10, txt=f"Precio Total: {solicitud.price} UF", ln=True)
    pdf.cell(200, 10, txt=f"Estado: {solicitud.estado}", ln=True)

    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=solicitud_{solicitud.id}.pdf'
    return response

@solicitudes_bp.route('/solicitudes_admin')
@login_required
def solicitudes_admin():
    solicitudes = Request.query.all()
    return render_template('admin_dashboard.html', section='solicitudes_admin', solicitudes=solicitudes)

# Ruta para cambiar estado
@solicitudes_bp.route('/cambiar_estado/<int:solicitud_id>', methods=['POST'])
@login_required
def cambiar_estado(solicitud_id):
    solicitud = Request.query.get_or_404(solicitud_id)
    nuevo_estado = request.form.get('estado')
    if nuevo_estado in ['Pendiente', 'Finalizado']:
        solicitud.estado = nuevo_estado
        db.session.commit()
        flash('Estado de la solicitud actualizado.', 'success')
    return redirect(url_for('solicitudes.solicitudes_admin'))

# Ruta para eliminar solicitud
@solicitudes_bp.route('/eliminar_solicitud/<int:solicitud_id>', methods=['POST'])
@login_required
def eliminar_solicitud(solicitud_id):
    solicitud = Request.query.get_or_404(solicitud_id)
    db.session.delete(solicitud)
    db.session.commit()
    flash('Solicitud eliminada.', 'success')
    return redirect(url_for('solicitudes.solicitudes_admin'))
