# Image Python 3.11
FROM python:3.11-slim

# Dossier de travail
WORKDIR /app

# Copie des fichiers requirements
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste du code
COPY . .

# Expose le port de Flask
EXPOSE 5001

# Lancement de l'application Flask
CMD ["python", "app.py"]
