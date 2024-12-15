#!/bin/bash

# Esperar a que la base de datos esté lista
echo "Esperando a que la base de datos esté disponible..."
while ! nc -z db 3306; do
  sleep 1
done
echo "La base de datos está lista."

# Aplicar migraciones
echo "Aplicando migraciones..."
flask db upgrade

# Crear roles
echo "Creando roles..."
python create_roles.py

# Crear usuario administrador
echo "Creando usuario administrador..."
python create_admin.py

# Iniciar la aplicación
echo "Iniciando la aplicación..."
exec python run.py