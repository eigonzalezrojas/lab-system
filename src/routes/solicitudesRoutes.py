from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_required, current_user
from src.services.solicitudes_service import (
    get_all_projects, get_all_machines, create_solicitud, get_admin_emails,
    send_solicitud_email, get_solicitud_by_id, delete_solicitud_by_id,
    update_solicitud_status, generate_solicitud_pdf
)
from src.services.email_service import send_email
from src.models import Request, Project, Machine, Solvent, Sample, Nucleo, SamplePreparation
from src.services.project_service import get_project_by_id
from src.services.machine_service import get_machine_by_id
from src.models import UserType
from src import db

solicitudes_bp = Blueprint('solicitudes', __name__)


@solicitudes_bp.route('/solicitudes')
@login_required
def solicitudes():
    projects = get_all_projects()
    machines = get_all_machines()

    # Obtener las solicitudes del usuario actual
    solicitudes = Request.query.filter_by(user_rut=current_user.rut).all()

    # Depuración para verificar los datos
    print(f"DEBUG: current_user.type = {current_user.type}")
    print(f"DEBUG: solicitudes = {solicitudes}")

    if current_user.type == UserType.INTERNAL:
        return render_template(
            'operador_dashboard_interno.html',
            section='solicitudes',
            projects=projects,
            machines=machines,
            solicitudes=solicitudes
        )
    elif current_user.type == UserType.EXTERNAL:
        return render_template(
            'operador_dashboard_externo.html',
            section='solicitudes',
            projects=projects,
            machines=machines,
            solicitudes=solicitudes
        )
    else:
        flash('Tipo de usuario no válido.', 'danger')
        return redirect(url_for('auth.logout'))


@solicitudes_bp.route('/solicitudes_admin')
@login_required
def solicitudes_admin():
    solicitudes = Request.query.order_by(Request.fecha.desc()).all()
    return render_template('admin_dashboard.html', section='solicitudes_admin', solicitudes=solicitudes)


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

    # Depuración para verificar el tipo de usuario
    print(f"DEBUG: current_user.type = {current_user.type}")

    if current_user.type == UserType.INTERNAL:
        return render_template(
            'operador_dashboard_interno.html',
            section='nueva_solicitud',
            project=project,
            machine=machine,
            solvents=solvents,
            sample_preparations=sample_preparations,
            samples=samples,
            nucleos=nucleos
        )
    elif current_user.type == UserType.EXTERNAL:
        return render_template(
            'operador_dashboard_externo.html',
            section='nueva_solicitud',
            project=project,
            machine=machine,
            solvents=solvents,
            sample_preparations=sample_preparations,
            samples=samples,
            nucleos=nucleos
        )
    else:
        flash('Tipo de usuario no válido.', 'danger')
        return redirect(url_for('auth.logout'))


@solicitudes_bp.route('/agregar_solicitud', methods=['POST'])
@login_required
def agregar_solicitud():
    try:
        # Obtener datos del formulario
        form_data = request.form
        sample_name = form_data.get('sample_name')

        # Obtener y validar el campo c13_grams
        c13_grams = form_data.get('c13_grams', '').strip()
        c13_grams = float(c13_grams) if c13_grams and c13_grams.replace('.', '', 1).isdigit() else None  # Si es inválido, lo deja como None

        # Lógica especial para la muestra C13 solo si fue seleccionada
        if sample_name and sample_name.upper() == "C13" and c13_grams is not None:
            sample = Sample.query.filter_by(name="C13").first()
            if sample:
                # Si los gramos son menores a 20, se multiplica el precio por 3
                if c13_grams < 15:
                    sample.precio_interno *= 3
                    sample.precio_externo *= 3
                sample.miligramos = int(c13_grams)
                db.session.commit()

        # Crear la solicitud excluyendo c13_grams si no aplica
        nueva_solicitud = create_solicitud(form_data, current_user)

        # Enviar correo a los administradores
        admin_emails = get_admin_emails()
        subject = "Nueva Solicitud Creada"
        body = f"""
            Una nueva solicitud ha sido creada en el sistema.

            Detalles de la Solicitud:
            - Nombre del Usuario: {nueva_solicitud.user_name}
            - Proyecto: {nueva_solicitud.project_name}
            - Muestra: {nueva_solicitud.request_name}
            - Fecha: {nueva_solicitud.fecha}
        """
        send_solicitud_email(send_email, subject, body, admin_emails)

        flash('Solicitud agregada con éxito', 'success')
        return redirect(url_for('solicitudes.solicitudes'))

    except Exception as e:
        db.session.rollback()
        flash(f'Ocurrió un error: {str(e)}', 'danger')
        return redirect(url_for('solicitudes.solicitudes'))


@solicitudes_bp.route('/descargar/<int:solicitud_id>', methods=['GET'])
@login_required
def descargar(solicitud_id):
    # Obtener la solicitud seleccionada
    solicitud = Request.query.get_or_404(solicitud_id)

    # Obtener todas las solicitudes asociadas al mismo proyecto y operador
    solicitudes = Request.query.filter_by(project_name=solicitud.project_name, user_rut=solicitud.user_rut).all()

    # Generar el PDF utilizando la función de servicio
    pdf = generate_solicitud_pdf(solicitud, solicitudes)

    # Preparar la respuesta con el PDF generado
    response = make_response(bytes(pdf.output(dest='S')))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=solicitud_{solicitud.id}.pdf'
    return response


@solicitudes_bp.route('/cambiar_estado/<int:solicitud_id>', methods=['POST'])
@login_required
def cambiar_estado(solicitud_id):
    nuevo_estado = request.form.get('estado')
    update_solicitud_status(solicitud_id, nuevo_estado)
    flash('Estado de la solicitud actualizado.', 'success')
    return redirect(url_for('solicitudes.solicitudes_admin'))


@solicitudes_bp.route('/eliminar_solicitud/<int:solicitud_id>', methods=['POST'])
@login_required
def eliminar_solicitud(solicitud_id):
    delete_solicitud_by_id(solicitud_id)
    flash('Solicitud eliminada.', 'success')
    return redirect(url_for('solicitudes.solicitudes_admin'))
