from src.models import Project, Machine, Solvent, SamplePreparation, Sample, Request, Nucleo, UserAccount, UserRole, UserType
from src import db
from fpdf import FPDF
from datetime import datetime
import pytz
import requests

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


def obtener_valor_uf():
    """Obtiene el valor actual de la UF desde la API de mindicador.cl."""
    try:
        # Realizar la solicitud a la API
        response = requests.get('https://mindicador.cl/api/uf', timeout=10)
        print(f"Estado de la respuesta: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"Datos obtenidos de la API: {data}")

            # Extraer el valor más reciente de la UF
            if "serie" in data and len(data["serie"]) > 0:
                valor_uf = data["serie"][0]["valor"]
                print(f"Valor actual de la UF: {valor_uf}")
                return valor_uf
            else:
                print("Error: No se encontró la serie de valores de la UF en la respuesta.")
                return None
        else:
            print(f"Error al obtener el valor de la UF: {response.status_code}")
            return None
    except requests.exceptions.Timeout:
        print("Error: La solicitud a la API de mindicador.cl excedió el tiempo de espera.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud a la API de mindicador.cl: {e}")
        return None
    except Exception as e:
        print(f"Excepción inesperada: {e}")
        return None
    

def create_solicitud(data, current_user):
    timezone = pytz.timezone('America/Santiago')
    current_time = datetime.now(timezone)

    sample_name = data.get('sample_name')
    solvent_id = data.get('solvent_id')
    sample_preparation_id = data.get('sample_preparation_id')
    recovery = data.get('recovery')
    sample_ids = data.getlist('sample_ids')
    nucleo_ids = data.getlist('nucleo_ids')
    machine_id = data.get('machine_id')

    samples = Sample.query.filter(Sample.id.in_(sample_ids)).all()
    nucleos = Nucleo.query.filter(Nucleo.id.in_(nucleo_ids)).all()
    machine = Machine.query.get(machine_id)

    total_cost = 0
    if current_user.type == UserType.INTERNAL:
        total_cost += sum(sample.precio_interno for sample in samples)
        total_cost += sum(nucleo.precio_interno for nucleo in nucleos)
    elif current_user.type == UserType.EXTERNAL:
        total_cost += sum(sample.precio_externo for sample in samples)
        total_cost += sum(nucleo.precio_externo for nucleo in nucleos)

    request_name = sample_name

    nueva_solicitud = Request(
        user_name=f"{current_user.first_name} {current_user.last_name}",
        user_rut=current_user.rut,
        project_name=data.get('project_name'),
        machine_name=machine.name,
        solvent_name=Solvent.query.get(solvent_id).name,
        sample_preparation_name=SamplePreparation.query.get(sample_preparation_id).name,
        recovery=recovery,
        request_name=request_name,
        sample_ids=','.join(map(str, sample_ids)),
        nucleo_ids=','.join(map(str, nucleo_ids)),
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

    valor_uf = obtener_valor_uf()
    if not valor_uf:
        raise Exception("No se pudo obtener el valor de la UF.")

    # Encabezado del PDF
    logo_path = 'src/static/img/utal.png'
    pdf.image(logo_path, x=10, y=8, w=30)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, 'Instituto de Química de Recursos Naturales', ln=True, align='C')

    pdf.ln(10)

    pdf.set_font("Arial", size=8)

    # Datos del Usuario
    pdf.cell(200, 6, txt="Datos del Usuario", ln=True, align='C')
    pdf.ln(6)
    pdf.cell(50, 6, txt="Nombre:", border=1)
    pdf.cell(140, 6, txt=f"{solicitud.user_name}", border=1, ln=True)
    pdf.cell(50, 6, txt="RUT:", border=1)
    pdf.cell(140, 6, txt=f"{solicitud.user_rut}", border=1, ln=True)
    pdf.cell(50, 6, txt="Email:", border=1)
    pdf.cell(140, 6, txt=f"{solicitud.user_rut}", border=1, ln=True)
    pdf.cell(50, 6, txt="Nombre del Proyecto:", border=1)
    pdf.cell(140, 6, txt=f"{solicitud.project_name}", border=1, ln=True)
    pdf.cell(50, 6, txt="Fecha:", border=1)
    pdf.cell(140, 6, txt=f"{solicitud.fecha.strftime('%Y-%m-%d %H:%M:%S')}", border=1, ln=True)

    pdf.ln(10)

    # Datos de la Solicitud
    pdf.cell(200, 6, txt="Datos de la Solicitud", ln=True, align='C')
    pdf.ln(6)

    pdf.cell(40, 6, txt="Nombre", border=1, align='C')
    pdf.cell(40, 6, txt="Máquina", border=1, align='C')
    pdf.cell(40, 6, txt="Solvente", border=1, align='C')
    pdf.cell(40, 6, txt="Preparación", border=1, align='C')
    pdf.cell(20, 6, txt="Recup.", border=1, align='C', ln=True)

    for solicitud_item in solicitudes:
        pdf.cell(40, 6, txt=f"{solicitud_item.request_name}", border=1, align='C')
        pdf.cell(40, 6, txt=f"{solicitud_item.machine_name}", border=1, align='C')
        pdf.cell(40, 6, txt=f"{solicitud_item.solvent_name}", border=1, align='C')
        pdf.cell(40, 6, txt=f"{solicitud_item.sample_preparation_name}", border=1, align='C')
        pdf.cell(20, 6, txt=f"{'Sí' if solicitud_item.recovery == 'si' else 'No'}", border=1, align='C', ln=True)

    pdf.ln(10)

    # Detalles de Experimentos y Núcleos
    pdf.cell(200, 6, txt="Detalles de Experimentos y Núcleos", ln=True, align='C')
    pdf.ln(6)

    unique_sample_ids = set()
    unique_nucleo_ids = set()

    for solicitud_item in solicitudes:
        unique_sample_ids.update(solicitud_item.sample_ids.split(','))
        unique_nucleo_ids.update(solicitud_item.nucleo_ids.split(','))

    selected_samples = Sample.query.filter(Sample.id.in_(unique_sample_ids)).all()
    selected_nucleos = Nucleo.query.filter(Nucleo.id.in_(unique_nucleo_ids)).all()

    total_width = 190
    static_columns_width = 40 + 20
    num_dynamic_columns = len(selected_samples) + len(selected_nucleos)

    if num_dynamic_columns > 0:
        dynamic_column_width = (total_width - static_columns_width) / num_dynamic_columns
    else:
        dynamic_column_width = 15

    if num_dynamic_columns > 5:
        pdf.set_font("Arial", size=6)
    else:
        pdf.set_font("Arial", size=8)

    table_width = static_columns_width + (dynamic_column_width * num_dynamic_columns)
    start_x = (210 - table_width) / 2
    pdf.set_x(start_x)

    pdf.cell(40, 6, txt="Nombre Solicitud", border=1, align='C')
    for sample in selected_samples:
        pdf.cell(dynamic_column_width, 6, txt=sample.name[:7], border=1, align='C')

    for nucleo in selected_nucleos:
        pdf.cell(dynamic_column_width, 6, txt=nucleo.nombre, border=1, align='C')

    pdf.cell(20, 6, txt="Monto (CLP)", border=1, align='C', ln=True)

    total_monto_clp = 0  # Variable para almacenar el total

    for solicitud_item in solicitudes:
        pdf.set_x(start_x)
        pdf.cell(40, 6, txt=f"{solicitud_item.request_name}", border=1, align='C')
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

        # Convertir el costo total a CLP
        total_cost_clp = solicitud_item.total_cost * valor_uf
        total_monto_clp += total_cost_clp  # Sumar al total
        pdf.cell(20, 6, txt=f"${total_cost_clp:,.0f}", border=1, align='C', ln=True)

    # Agregar el total al final de la tabla
    pdf.ln(6)
    pdf.set_x(start_x)
    pdf.set_font("Arial", style="B", size=8)
    pdf.cell(40 + dynamic_column_width * num_dynamic_columns, 6, txt="TOTAL", border=1, align='L')
    pdf.cell(20, 6, txt=f"${total_monto_clp:,.0f}", border=1, align='C', ln=True)

    return pdf

def get_all_solicitudes_with_details(user_rut):
    solicitudes = Request.query.filter_by(user_rut=user_rut).all()
    solicitudes_data = []
    for solicitud in solicitudes:
        solicitudes_data.append({
            'id': solicitud.id,
            'request_name': solicitud.request_name,
            'user_name': solicitud.user_name,
            'project_name': solicitud.project_name,
            'machine_name': solicitud.machine_name,
            'fecha': solicitud.fecha,
            'estado': solicitud.estado,
            'total_cost': solicitud.total_cost
        })
    return solicitudes_data