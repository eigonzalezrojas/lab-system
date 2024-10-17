from src.models import UserAccount, Project, Machine, Solvent, Sample, SamplePreparation, Request, Nucleo


def get_statistics():
    total_usuarios = UserAccount.query.count()
    total_proyectos = Project.query.count()
    total_maquinas = Machine.query.count()
    total_solventes = Solvent.query.count()
    total_muestras = Sample.query.count()
    total_preparaciones = SamplePreparation.query.count()
    total_nucleos = Nucleo.query.count()
    total_solicitudes = Request.query.count()

    return {
        'total_usuarios': total_usuarios,
        'total_proyectos': total_proyectos,
        'total_maquinas': total_maquinas,
        'total_solventes': total_solventes,
        'total_muestras': total_muestras,
        'total_preparaciones': total_preparaciones,
        'total_nucleos': total_nucleos,
        'total_solicitudes': total_solicitudes
    }


def get_operator_statistics(solicitudes):
    total_solicitudes = len(solicitudes)
    total_proyectos = Project.query.count()

    # Calcular el total de facturas (sumando el costo total de las solicitudes)
    total_facturas = sum(solicitud.total_cost for solicitud in solicitudes)

    return {
        'total_solicitudes': total_solicitudes,
        'total_proyectos': total_proyectos,
        'total_facturas': total_facturas,
    }