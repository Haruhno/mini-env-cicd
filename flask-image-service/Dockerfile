# Image Python 3.11
FROM python:3.11-slim

# Dossier de travail
WORKDIR /app

# Copie les fichiers requirements si tu en as un
COPY flask-image-service/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste du code
COPY flask-image-service/ .

# Expose le port de Flask
EXPOSE 5000

# Lancement de l'application Flask
CMD ["python", "app.py"]
