from flask import Blueprint, render_template, request, make_response, redirect, url_for, flash
from flask_login import login_required, current_user
from src.models import Project, Machine, Solvent, SamplePreparation, Sample, Request, Nucleo
from src import db
from fpdf import FPDF
from datetime import datetime

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
    nucleos = Nucleo.query.all()

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
        nucleos=nucleos
    )

@solicitudes_bp.route('/agregar_solicitud', methods=['POST'])
@login_required
def agregar_solicitud():
    sample_name = request.form.get('sample_name')  # Obtener el nombre de la muestra desde el formulario
    solvent_id = request.form.get('solvent_id')
    sample_preparation_id = request.form.get('sample_preparation_id')
    recovery = request.form.get('recovery')
    sample_ids = request.form.getlist('sample_ids')
    nucleo_ids = request.form.getlist('nucleo_ids')

    # Obtener y procesar muestras y núcleos
    samples = Sample.query.filter(Sample.id.in_(sample_ids)).all()
    nucleos = Nucleo.query.filter(Nucleo.id.in_(nucleo_ids)).all()

    # Calcular el precio total
    total_cost = sum(sample.price for sample in samples) + sum(nucleo.precio for nucleo in nucleos)

    # Usar el nombre de la muestra proporcionado por el usuario como el request_name
    request_name = sample_name

    # Crear una nueva solicitud
    nueva_solicitud = Request(
        user_name=current_user.first_name + " " + current_user.last_name,
        user_rut=current_user.rut,
        project_name=request.form.get('project_name'),
        solvent_name=Solvent.query.get(solvent_id).name,
        sample_preparation_name=SamplePreparation.query.get(sample_preparation_id).name,
        recovery=recovery,
        request_name=request_name,  # Asignar request_name basado en el nombre de la muestra
        sample_ids=','.join(sample_ids),
        nucleo_ids=','.join(nucleo_ids),
        total_cost=total_cost,
        estado='Pendiente'
    )

    db.session.add(nueva_solicitud)
    db.session.commit()

    flash('Solicitud agregada con éxito', 'success')
    return redirect(url_for('solicitudes.solicitudes'))


@solicitudes_bp.route('/descargar/<int:solicitud_id>', methods=['GET'])
@login_required
def descargar(solicitud_id):
    # Obtener la solicitud seleccionada
    solicitud = Request.query.get_or_404(solicitud_id)

    # Obtener todas las solicitudes asociadas al mismo proyecto
    solicitudes = Request.query.filter_by(project_name=solicitud.project_name).all()

    # Crear PDF
    pdf = FPDF()
    pdf.add_page()

    # Reducir el tamaño de la fuente
    pdf.set_font("Arial", size=8)

    # Ancho total disponible para la tabla
    total_width = 190  # El ancho total de una página A4 menos márgenes
    static_columns_width = 20 + 20 + 20 + 15 + 20  # Ancho de las columnas estáticas (Nombre, Solvente, etc.)

    # Obtener todas las muestras y núcleos
    all_samples = Sample.query.all()
    all_nucleos = Nucleo.query.all()

    # Número de columnas dinámicas (muestras + núcleos)
    num_dynamic_columns = len(all_samples) + len(all_nucleos)

    # Calcular el ancho de cada columna dinámica
    if num_dynamic_columns > 0:
        dynamic_column_width = (total_width - static_columns_width) / num_dynamic_columns
    else:
        dynamic_column_width = 15  # Un valor por defecto en caso de no haber columnas dinámicas

    # Tabla con información del operador
    pdf.cell(200, 6, txt="Datos del Usuario", ln=True, align='C')
    pdf.ln(6)
    pdf.cell(50, 6, txt="Nombre:", border=1)
    pdf.cell(140, 6, txt=f"{solicitud.user_name}", border=1, ln=True)
    pdf.cell(50, 6, txt="RUT:", border=1)
    pdf.cell(140, 6, txt=f"{solicitud.user_rut}", border=1, ln=True)
    pdf.cell(50, 6, txt="Email:", border=1)
    pdf.cell(140, 6, txt=f"{current_user.email}", border=1, ln=True)
    pdf.cell(50, 6, txt="Nombre del Proyecto:", border=1)
    pdf.cell(140, 6, txt=f"{solicitud.project_name}", border=1, ln=True)
    pdf.cell(50, 6, txt="Fecha:", border=1)
    pdf.cell(140, 6, txt=f"{solicitud.fecha.strftime('%Y-%m-%d %H:%M:%S')}", border=1, ln=True)

    pdf.ln(6)

    # Tabla combinada de datos de la solicitud, muestras y núcleos
    pdf.cell(200, 6, txt="Datos de la Solicitud", ln=True, align='C')
    pdf.ln(6)

    # Cabecera de la tabla
    pdf.cell(20, 6, txt="Nombre", border=1, align='C')
    pdf.cell(20, 6, txt="Solvente", border=1, align='C')
    pdf.cell(20, 6, txt="Preparación", border=1, align='C')
    pdf.cell(15, 6, txt="Recup.", border=1, align='C')

    # Añadir cabecera de muestras
    for sample in all_samples:
        pdf.cell(dynamic_column_width, 6, txt=sample.name[:7], border=1, align='C')

    # Añadir cabecera de núcleos
    for nucleo in all_nucleos:
        pdf.cell(dynamic_column_width, 6, txt=nucleo.nombre[:7], border=1, align='C')

    pdf.cell(20, 6, txt="Total (UF)", border=1, align='C', ln=True)

    # Inicializar contadores para el total de muestras y total de la orden
    total_muestras = 0
    total_orden = 0

    # Fila de datos para cada solicitud asociada al proyecto
    for solicitud in solicitudes:
        pdf.cell(20, 6, txt=f"{solicitud.request_name}", border=1, align='C')
        pdf.cell(20, 6, txt=f"{solicitud.solvent_name}", border=1, align='C')
        pdf.cell(20, 6, txt=f"{solicitud.sample_preparation_name}", border=1, align='C')
        pdf.cell(15, 6, txt=f"{'Sí' if solicitud.recovery == 'si' else 'No'}", border=1, align='C')

        # Fila de "X" o vacío para muestras
        selected_sample_ids = solicitud.sample_ids.split(',')
        total_muestras += len(selected_sample_ids)
        for sample in all_samples:
            if str(sample.id) in selected_sample_ids:
                pdf.cell(dynamic_column_width, 6, txt="X", border=1, align='C')
            else:
                pdf.cell(dynamic_column_width, 6, txt="", border=1, align='C')

        # Fila de "X" o vacío para núcleos
        selected_nucleo_ids = solicitud.nucleo_ids.split(',')
        for nucleo in all_nucleos:
            if str(nucleo.id) in selected_nucleo_ids:
                pdf.cell(dynamic_column_width, 6, txt="X", border=1, align='C')
            else:
                pdf.cell(dynamic_column_width, 6, txt="", border=1, align='C')

        # Sumar el total de la solicitud al total de la orden
        total_orden += solicitud.total_cost
        pdf.cell(20, 6, txt=f"{solicitud.total_cost} UF", border=1, align='C', ln=True)

    pdf.ln(10)

    # Calcular posición centrada para "N° de muestras" y "Total orden"
    left_margin = (210 - (50 + 100)) / 2  # 210 es el ancho de una página A4 en mm

    # Centrar la sección de "N° de muestras" y "Total orden"
    pdf.set_x(left_margin)
    pdf.cell(50, 6, txt=f"N° de muestras: {total_muestras}", border=1, align='L')
    pdf.cell(100, 6, txt=f"Total orden: {total_orden} UF", border=1, align='R', ln=True)

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