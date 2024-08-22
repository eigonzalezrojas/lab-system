# Utiliza la imagen base de Python 3.9 slim
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de dependencias en el contenedor
COPY requirements.txt requirements.txt

# Crea y activa un entorno virtual
RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código fuente del proyecto en el contenedor
COPY . .

# Especifica el puerto en el que la aplicación estará disponible
EXPOSE 5000

# Utiliza Gunicorn con 4 workers, enlazando al puerto 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "src:app"]
