# Utilise l'image officielle OpenJDK 17
FROM openjdk:17-jdk-slim

# Crée le dossier de travail
WORKDIR /app

# Copie le fichier JAR (après compilation)
COPY target/imageupload-0.0.1-SNAPSHOT.jar app.jar

# Expose le port de l'application
EXPOSE 8080

# Commande pour lancer l'application
ENTRYPOINT ["java", "-jar", "app.jar"]
