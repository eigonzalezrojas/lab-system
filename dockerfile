# Usa la imagen base de Python 3.9 slim, que es ligera y contiene solo lo necesario para ejecutar Python
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor. Todo el código será copiado y ejecutado desde aquí
WORKDIR /app

# Copia el archivo de dependencias en el contenedor para instalar las bibliotecas necesarias
COPY requirements.txt requirements.txt

# Instala las dependencias listadas en requirements.txt directamente en el sistema del contenedor
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente del proyecto dentro del contenedor
COPY . .

# Expone el puerto 5000, que es donde Flask servirá la aplicación
EXPOSE 5000

# Define el comando por defecto para iniciar la aplicación Flask
CMD ["python", "run.py"]