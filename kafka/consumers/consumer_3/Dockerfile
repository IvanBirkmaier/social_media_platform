# Verwenden Sie ein offizielles Python-Laufzeit-Image als Basis
FROM python:3.9

# Setzen Sie das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopieren Sie die Python-Abhängigkeiten in den Container
COPY requirements.txt /app/

# Oder Ihre Kafka-Server-Adresse
ENV KAFKA_BOOTSTRAP_SERVERS=localhost:9092  
ENV KAFKA_TOPIC=comment_queue


# Installieren Sie Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren Sie den Consumer-Code in den Container
COPY . /app/

# Standard-Kommando, um den Kafka Consumer zu starten
CMD ["python", "consumer.py"]
