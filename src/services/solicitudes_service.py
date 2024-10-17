from src.models import Project, Machine, Solvent, SamplePreparation, Sample, Request, Nucleo, UserAccount, UserRole
from src import db
from fpdf import FPDF
from datetime import datetime
import pytz


def get_all_projects():
    return Project.query.all()


def get_all_machines():
    return Machine.query.all()


def get_all_solvents():
    return Solvent.query.all()


def get_all_sample_preparations():
    return SamplePreparation.query.all()


def get_all_samples():
    return Sample.query.all()


def get_all_nucleos():
    return Nucleo.query.all()


def create_solicitud(data, current_user):
    # Configurar la zona horaria de Santiago
    timezone = pytz.timezone('America/Santiago')
    current_time = datetime.now(timezone)

    # Obtener los datos de la solicitud
    sample_name = data.get('sample_name')
    solvent_id = data.get('solvent_id')
    sample_preparation_id = data.get('sample_preparation_id')
    recovery = data.get('recovery')
    sample_ids = data.getlist('sample_ids')
    nucleo_ids = data.getlist('nucleo_ids')
    machine_id = data.get('machine_id')

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
        user_name=f"{current_user.first_name} {current_user.last_name}",
        user_rut=current_user.rut,
        project_name=data.get('project_name'),
        machine_name=machine.name,
        solvent_name=Solvent.query.get(solvent_id).name,
        sample_preparation_name=SamplePreparation.query.get(sample_preparation_id).name,
        recovery=recovery,
        request_name=request_name,
        sample_ids=','.join(sample_ids),
        nucleo_ids=','.join(nucleo_ids),
        total_cost=total_cost,
        estado='Pendiente',
        fecha=current_time
    )

    db.session.add(nueva_solicitud)
    db.session.commit()

    return nueva_solicitud


def get_admin_emails():
    admin_users = UserAccount.query.join(UserRole).filter(UserRole.name == 'administrador').all()
    return [user.email for user in admin_users]


def send_solicitud_email(send_email_function, subject, body, admin_emails):
    for email in admin_emails:
        send_email_function(subject, email, body)

def get_solicitud_by_id(solicitud_id):
    return Request.query.get_or_404(solicitud_id)


def delete_solicitud_by_id(solicitud_id):
    solicitud = Request.query.get_or_404(solicitud_id)
    db.session.delete(solicitud)
    db.session.commit()


def update_solicitud_status(solicitud_id, nuevo_estado):
    solicitud = Request.query.get_or_404(solicitud_id)
    solicitud.estado = nuevo_estado
    db.session.commit()


def generate_solicitud_pdf(solicitud, solicitudes):
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
    pdf.cell(140, 6, txt=f"{solicitud.user_rut}", border=1, ln=True)  # Email es current_user.email
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
    for solicitud_item in solicitudes:
        pdf.cell(40, 6, txt=f"{solicitud_item.request_name}", border=1, align='C')
        pdf.cell(40, 6, txt=f"{solicitud_item.machine_name}", border=1, align='C')
        pdf.cell(40, 6, txt=f"{solicitud_item.solvent_name}", border=1, align='C')
        pdf.cell(40, 6, txt=f"{solicitud_item.sample_preparation_name}", border=1, align='C')
        pdf.cell(20, 6, txt=f"{'Sí' if solicitud_item.recovery == 'si' else 'No'}", border=1, align='C', ln=True)

    pdf.ln(10)  # Espacio entre las dos partes de la tabla de solicitud

    # **Segunda parte de la segunda sección: Experimentos, Núcleos, y Total**
    pdf.cell(200, 6, txt="Detalles de Experimentos y Núcleos", ln=True, align='C')
    pdf.ln(6)

    # Recopilar todos los experimentos y núcleos únicos
    unique_sample_ids = set()
    unique_nucleo_ids = set()

    for solicitud_item in solicitudes:
        unique_sample_ids.update(solicitud_item.sample_ids.split(','))
        unique_nucleo_ids.update(solicitud_item.nucleo_ids.split(','))

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
    for solicitud_item in solicitudes:
        pdf.set_x(start_x)  # Reajustar la posición x para cada fila
        pdf.cell(40, 6, txt=f"{solicitud_item.request_name}", border=1, align='C')  # Nombre de la Solicitud
        for sample in selected_samples:
            if str(sample.id) in solicitud_item.sample_ids.split(','):
                pdf.cell(dynamic_column_width, 6, txt="X", border=1, align='C')
            else:
                pdf.cell(dynamic_column_width, 6, txt="", border=1, align='C')

        for nucleo in selected_nucleos:
            if str(nucleo.id) in solicitud_item.nucleo_ids.split(','):
                pdf.cell(dynamic_column_width, 6, txt="X", border=1, align='C')
            else:
                pdf.cell(dynamic_column_width, 6, txt="", border=1, align='C')

        pdf.cell(20, 6, txt=f"{solicitud_item.total_cost} UF", border=1, align='C', ln=True)

    return pdf
