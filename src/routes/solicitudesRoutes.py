from flask import Blueprint, render_template, request, make_response, redirect, url_for, flash
from flask_login import login_required, current_user
from src.models import Project, Machine, Solvent, SamplePreparation, Sample, Request, Nucleo, UserAccount, UserRole
from src import db
from fpdf import FPDF
from .authRoutes import send_email
from datetime import datetime
import pytz

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
    # Configurar la zona horaria de Santiago
    timezone = pytz.timezone('America/Santiago')
    current_time = datetime.now(timezone)

    sample_name = request.form.get('sample_name')
    solvent_id = request.form.get('solvent_id')
    sample_preparation_id = request.form.get('sample_preparation_id')
    recovery = request.form.get('recovery')
    sample_ids = request.form.getlist('sample_ids')
    nucleo_ids = request.form.getlist('nucleo_ids')
    machine_id = request.form.get('machine_id')

    # Obtener y procesar muestras y núcleos
    samples = Sample.query.filter(Sample.id.in_(sample_ids)).all()
    nucleos = Nucleo.query.filter(Nucleo.id.in_(nucleo_ids)).all()
    machine = Machine.query.get(machine_id)

    # Calcular el precio total
    total_cost = sum(sample.price for sample in samples) + sum(nucleo.precio for nucleo in nucleos)

    # Usar el nombre de la muestra proporcionado por el usuario como el request_name
    request_name = sample_name

    # Crear una nueva solicitud
    nueva_solicitud = Request(
        user_name=current_user.first_name + " " + current_user.last_name,
        user_rut=current_user.rut,
        project_name=request.form.get('project_name'),
        machine_name=machine.name,
        solvent_name=Solvent.query.get(solvent_id).name,
        sample_preparation_name=SamplePreparation.query.get(sample_preparation_id).name,
        recovery=recovery,
        request_name=request_name,
        sample_ids=','.join(sample_ids),
        nucleo_ids=','.join(nucleo_ids),
        total_cost=total_cost,
        estado='Pendiente',
        fecha = current_time
    )

    db.session.add(nueva_solicitud)
    db.session.commit()

    # Obtener correos de los administradores
    admin_users = UserAccount.query.join(UserRole).filter(UserRole.name == 'administrador').all()
    admin_emails = [user.email for user in admin_users]

    # Enviar correo a los administradores
    subject = "Nueva Solicitud Creada"
    body = f"""
            Una nueva solicitud ha sido creada en el sistema.

            Detalles de la Solicitud:
            - Nombre del Usuario: {nueva_solicitud.user_name}
            - Proyecto: {nueva_solicitud.project_name}
            - Muestra: {nueva_solicitud.request_name}
            - Fecha: {nueva_solicitud.fecha}

            Por favor, revisa la solicitud en el sistema.
            """

    for email in admin_emails:
        send_email(subject, email, body)

    flash('Solicitud agregada con éxito', 'success')
    return redirect(url_for('solicitudes.solicitudes'))

@solicitudes_bp.route('/descargar/<int:solicitud_id>', methods=['GET'])
@login_required
def descargar(solicitud_id):
    # Obtener la solicitud seleccionada
    solicitud = Request.query.get_or_404(solicitud_id)

    # Obtener todas las solicitudes asociadas al mismo proyecto y operador
    solicitudes = Request.query.filter_by(project_name=solicitud.project_name, user_rut=current_user.rut).all()

    # Crear PDF
    pdf = FPDF()
    pdf.add_page()

    # Agregar logo y frase
    logo_path = 'src/static/img/utal.png'
    pdf.image(logo_path, x=10, y=8, w=30)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, 'Instituto de Química de Recursos Naturales', ln=True, align='C')

    # Espacio debajo del logo y frase
    pdf.ln(10)

    # Reducir el tamaño de la fuente
    pdf.set_font("Arial", size=8)

    # **Primera sección: Información del Usuario**
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

    pdf.ln(10)  # Espacio entre secciones

    # **Primera parte de la segunda sección: Información básica de la solicitud**
    pdf.cell(200, 6, txt="Datos de la Solicitud", ln=True, align='C')
    pdf.ln(6)

    # Cabecera de la primera parte de la tabla de solicitud
    pdf.cell(40, 6, txt="Nombre", border=1, align='C')
    pdf.cell(40, 6, txt="Máquina", border=1, align='C')
    pdf.cell(40, 6, txt="Solvente", border=1, align='C')
    pdf.cell(40, 6, txt="Preparación", border=1, align='C')
    pdf.cell(20, 6, txt="Recup.", border=1, align='C', ln=True)

    # Filas de la primera parte de la tabla de solicitud
    for solicitud in solicitudes:
        pdf.cell(40, 6, txt=f"{solicitud.request_name}", border=1, align='C')
        pdf.cell(40, 6, txt=f"{solicitud.machine_name}", border=1, align='C')
        pdf.cell(40, 6, txt=f"{solicitud.solvent_name}", border=1, align='C')
        pdf.cell(40, 6, txt=f"{solicitud.sample_preparation_name}", border=1, align='C')
        pdf.cell(20, 6, txt=f"{'Sí' if solicitud.recovery == 'si' else 'No'}", border=1, align='C', ln=True)

    pdf.ln(10)  # Espacio entre las dos partes de la tabla de solicitud

    # **Segunda parte de la segunda sección: Experimentos, Núcleos, y Total**
    pdf.cell(200, 6, txt="Detalles de Experimentos y Núcleos", ln=True, align='C')
    pdf.ln(6)

    # Recopilar todos los experimentos y núcleos únicos
    unique_sample_ids = set()
    unique_nucleo_ids = set()

    for solicitud in solicitudes:
        unique_sample_ids.update(solicitud.sample_ids.split(','))
        unique_nucleo_ids.update(solicitud.nucleo_ids.split(','))

    selected_samples = Sample.query.filter(Sample.id.in_(unique_sample_ids)).all()
    selected_nucleos = Nucleo.query.filter(Nucleo.id.in_(unique_nucleo_ids)).all()

    # Ajuste del tamaño de las columnas dinámicas para que la tabla no sea demasiado ancha
    total_width = 190  # Ancho total disponible
    static_columns_width = 40 + 20  # Ancho de las columnas fijas (Nombre Solicitud + Total)
    num_dynamic_columns = len(selected_samples) + len(selected_nucleos)

    # Calcular el ancho de cada columna dinámica
    if num_dynamic_columns > 0:
        dynamic_column_width = (total_width - static_columns_width) / num_dynamic_columns
    else:
        dynamic_column_width = 15  # Un valor por defecto en caso de no haber columnas dinámicas

    # Ajustar tamaño de letra basado en el número de columnas
    if num_dynamic_columns > 5:
        pdf.set_font("Arial", size=6)
    else:
        pdf.set_font("Arial", size=8)

    # Centrar la tabla en la página
    table_width = static_columns_width + (dynamic_column_width * num_dynamic_columns)
    start_x = (210 - table_width) / 2  # Centrado basado en una página A4 de 210mm
    pdf.set_x(start_x)

    # Cabecera de la segunda parte de la tabla de solicitud
    pdf.cell(40, 6, txt="Nombre Solicitud", border=1, align='C')  # Nombre de la Solicitud
    for sample in selected_samples:
        pdf.cell(dynamic_column_width, 6, txt=sample.name[:7], border=1, align='C')

    for nucleo in selected_nucleos:
        pdf.cell(dynamic_column_width, 6, txt=nucleo.nombre[:7], border=1, align='C')

    pdf.cell(20, 6, txt="Total (UF)", border=1, align='C', ln=True)

    # Filas de la segunda parte de la tabla de solicitud
    for solicitud in solicitudes:
        pdf.set_x(start_x)  # Reajustar la posición x para cada fila
        pdf.cell(40, 6, txt=f"{solicitud.request_name}", border=1, align='C')  # Nombre de la Solicitud
        for sample in selected_samples:
            if str(sample.id) in solicitud.sample_ids.split(','):
                pdf.cell(dynamic_column_width, 6, txt="X", border=1, align='C')
            else:
                pdf.cell(dynamic_column_width, 6, txt="", border=1, align='C')

        for nucleo in selected_nucleos:
            if str(nucleo.id) in solicitud.nucleo_ids.split(','):
                pdf.cell(dynamic_column_width, 6, txt="X", border=1, align='C')
            else:
                pdf.cell(dynamic_column_width, 6, txt="", border=1, align='C')

        pdf.cell(20, 6, txt=f"{solicitud.total_cost} UF", border=1, align='C', ln=True)

    pdf.ln(10)

    # Calcular posición centrada para "N° de solicitudes" y "Total orden"
    left_margin = (210 - (50 + 100)) / 2  # 210 es el ancho de una página A4 en mm

    # Centrar la sección de "N° de solicitudes" y "Total orden"
    pdf.set_x(left_margin)
    pdf.cell(50, 6, txt=f"N° de solicitudes: {len(solicitudes)}", border=1, align='L')
    pdf.cell(100, 6, txt=f"Total orden: {sum([solicitud.total_cost for solicitud in solicitudes])} UF", border=1, align='R', ln=True)

    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=solicitud_{solicitud.id}.pdf'
    return response


@solicitudes_bp.route('/admin_descargar/<int:solicitud_id>', methods=['GET'])
@login_required
def admin_descargar(solicitud_id):
    # Obtener la solicitud seleccionada
    solicitud = Request.query.get_or_404(solicitud_id)

    # Obtener todas las solicitudes asociadas al mismo proyecto y operador
    solicitudes = Request.query.filter_by(project_name=solicitud.project_name, user_rut=solicitud.user_rut).all()

    # Crear el PDF
    pdf = FPDF()
    pdf.add_page()

    # Agregar logo y frase
    logo_path = 'src/static/img/utal.png'
    pdf.image(logo_path, x=10, y=8, w=30)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, 'Instituto de Química de Recursos Naturales', ln=True, align='C')

    # Espacio debajo del logo y frase
    pdf.ln(10)

    # Reducir el tamaño de la fuente
    pdf.set_font("Arial", size=8)

    # **Primera sección: Información del Usuario**
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

    pdf.ln(10)  # Espacio entre secciones

    # **Primera parte de la segunda sección: Información básica de la solicitud**
    pdf.cell(200, 6, txt="Datos de la Solicitud", ln=True, align='C')
    pdf.ln(6)

    # Cabecera de la primera parte de la tabla de solicitud
    pdf.cell(40, 6, txt="Nombre", border=1, align='C')
    pdf.cell(40, 6, txt="Máquina", border=1, align='C')
    pdf.cell(40, 6, txt="Solvente", border=1, align='C')
    pdf.cell(40, 6, txt="Preparación", border=1, align='C')
    pdf.cell(20, 6, txt="Recup.", border=1, align='C', ln=True)

    # Filas de la primera parte de la tabla de solicitud
    for solicitud in solicitudes:
        pdf.cell(40, 6, txt=f"{solicitud.request_name}", border=1, align='C')
        pdf.cell(40, 6, txt=f"{solicitud.machine_name}", border=1, align='C')
        pdf.cell(40, 6, txt=f"{solicitud.solvent_name}", border=1, align='C')
        pdf.cell(40, 6, txt=f"{solicitud.sample_preparation_name}", border=1, align='C')
        pdf.cell(20, 6, txt=f"{'Sí' if solicitud.recovery == 'si' else 'No'}", border=1, align='C', ln=True)

    pdf.ln(10)  # Espacio entre las dos partes de la tabla de solicitud

    # **Segunda parte de la segunda sección: Experimentos, Núcleos, y Total**
    pdf.cell(200, 6, txt="Detalles de Experimentos y Núcleos", ln=True, align='C')
    pdf.ln(6)

    # Recopilar todos los experimentos y núcleos únicos
    unique_sample_ids = set()
    unique_nucleo_ids = set()

    for solicitud in solicitudes:
        unique_sample_ids.update(solicitud.sample_ids.split(','))
        unique_nucleo_ids.update(solicitud.nucleo_ids.split(','))

    selected_samples = Sample.query.filter(Sample.id.in_(unique_sample_ids)).all()
    selected_nucleos = Nucleo.query.filter(Nucleo.id.in_(unique_nucleo_ids)).all()

    # Ajuste del tamaño de las columnas dinámicas para que la tabla no sea demasiado ancha
    total_width = 190  # Ancho total disponible
    static_columns_width = 40 + 20  # Ancho de las columnas fijas (Nombre Solicitud + Total)
    num_dynamic_columns = len(selected_samples) + len(selected_nucleos)

    # Calcular el ancho de cada columna dinámica
    if num_dynamic_columns > 0:
        dynamic_column_width = (total_width - static_columns_width) / num_dynamic_columns
    else:
        dynamic_column_width = 15  # Un valor por defecto en caso de no haber columnas dinámicas

    # Ajustar tamaño de letra basado en el número de columnas
    if num_dynamic_columns > 5:
        pdf.set_font("Arial", size=6)
    else:
        pdf.set_font("Arial", size=8)

    # Centrar la tabla en la página
    table_width = static_columns_width + (dynamic_column_width * num_dynamic_columns)
    start_x = (210 - table_width) / 2  # Centrado basado en una página A4 de 210mm
    pdf.set_x(start_x)

    # Cabecera de la segunda parte de la tabla de solicitud
    pdf.cell(40, 6, txt="Nombre Solicitud", border=1, align='C')  # Nombre de la Solicitud
    for sample in selected_samples:
        pdf.cell(dynamic_column_width, 6, txt=sample.name[:7], border=1, align='C')

    for nucleo in selected_nucleos:
        pdf.cell(dynamic_column_width, 6, txt=nucleo.nombre[:7], border=1, align='C')

    pdf.cell(20, 6, txt="Total (UF)", border=1, align='C', ln=True)

    # Filas de la segunda parte de la tabla de solicitud
    for solicitud in solicitudes:
        pdf.set_x(start_x)  # Reajustar la posición x para cada fila
        pdf.cell(40, 6, txt=f"{solicitud.request_name}", border=1, align='C')  # Nombre de la Solicitud
        for sample in selected_samples:
            if str(sample.id) in solicitud.sample_ids.split(','):
                pdf.cell(dynamic_column_width, 6, txt="X", border=1, align='C')
            else:
                pdf.cell(dynamic_column_width, 6, txt="", border=1, align='C')

        for nucleo in selected_nucleos:
            if str(nucleo.id) in solicitud.nucleo_ids.split(','):
                pdf.cell(dynamic_column_width, 6, txt="X", border=1, align='C')
            else:
                pdf.cell(dynamic_column_width, 6, txt="", border=1, align='C')

        pdf.cell(20, 6, txt=f"{solicitud.total_cost} UF", border=1, align='C', ln=True)

    pdf.ln(10)

    # Calcular posición centrada para "N° de solicitudes" y "Total orden"
    left_margin = (210 - (50 + 100)) / 2  # 210 es el ancho de una página A4 en mm

    # Centrar la sección de "N° de solicitudes" y "Total orden"
    pdf.set_x(left_margin)
    pdf.cell(50, 6, txt=f"N° de solicitudes: {len(solicitudes)}", border=1, align='L')
    pdf.cell(100, 6, txt=f"Total orden: {sum([solicitud.total_cost for solicitud in solicitudes])} UF", border=1, align='R', ln=True)

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