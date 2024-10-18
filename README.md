# Lab System

Este proyecto es un sistema de gestión para un laboratorio de química, que permite gestionar solicitudes de compuestos químicos, usuarios, proyectos y máquinas, entre otras funcionalidades.

## Tecnologías utilizadas

- **Backend**: Flask (Python)
- **Frontend**: Tailwind CSS
- **Base de datos**: MariaDB
- **Contenerización**: Docker y Docker Compose

## Instalación

### Requisitos previos

Asegúrate de tener instalado lo siguiente en tu sistema:

- Docker
- Docker Compose

### Clonar el repositorio

```bash
git clone https://github.com/eigonzalezrojas/lab-system.git
cd lab-system
```

### Configuración del entorno

Crea un archivo .env en la raíz del proyecto con el siguiente contenido:

- MYSQL_ROOT_PASSWORD=your_root_password
- MYSQL_DATABASE=lab_db
- MYSQL_USER=your_user
- MYSQL_PASSWORD=your_password
- FLASK_APP=src
- FLASK_ENV=development

### Construcción e inicio de los contenedores

```bash
docker-compose up --build
```

### Migraciones de base de datos
```bash
docker-compose exec web flask db upgrade
```

### Funcionalidades

#### Dashboard de Operadores

	•	Ver y gestionar solicitudes de muestras.
	•	Enviar nuevas solicitudes.
	•	Cambiar la contraseña.

#### Dashboard de Administradores

	•	Gestión de usuarios, proyectos, máquinas, solventes y más.
	•	Modificación y eliminación de registros.
	•	Resumen de estadísticas generales.

#### Tailwind CSS

El diseño del frontend está construido utilizando Tailwind CSS para una personalización rápida y eficiente de los estilos, con menús interactivos y transiciones suaves.
