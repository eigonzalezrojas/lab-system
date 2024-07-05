FROM python:3.9-slim
WORKDIR /Users/eithelgonzalez/Library/CloudStorage/OneDrive-Personal/Documentos/Eithel/DevProjects/lab-system
COPY requirements.txt requirements.txt
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "run.py"]
