# Verwenden Sie das offizielle Python-Image als Basis
FROM python:3.9

# Setzen Sie das Arbeitsverzeichnis im Container
WORKDIR /code

# Installieren Sie die Abhängigkeiten
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Kopieren Sie den Quellcode in den Container
COPY ./src /code/src
COPY app.py /code/

ENV KAFKA_TOPIC=classified_comments_queue
ENV KAFKA_BOOTSTRAP_SERVERS=localhost:9092


# Gesundheitscheck (optional, angepasst an Ihre App)
#HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
 #   CMD curl -f http://localhost:8002/ || exit 1

# Legen Sie den Befehl fest, um die Anwendung auszuführen
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8007"]

# Legen Sie den Port fest, auf dem die Anwendung laufen soll
EXPOSE 8007
