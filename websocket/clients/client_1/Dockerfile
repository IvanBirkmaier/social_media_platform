# Verwenden eines offiziellen Python-Images als Basis
FROM python:3.9

# Setzen des Arbeitsverzeichnisses im Container
WORKDIR /app

# Kopieren der Abhängigkeiten-Datei und Installieren der erforderlichen Pakete
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren des src-Verzeichnisses in das Arbeitsverzeichnis des Containers



COPY ./src /app/src
COPY app.py /app/
# Kopieren der Hauptanwendung und der .env-Datei in das Arbeitsverzeichnis
# COPY .env .

# Exponieren des Ports, auf dem der FastAPI-Server läuft
EXPOSE 8003

# Setzen von Umgebungsvariablen
ENV WEBSOCKET_SERVER_HOST=0.0.0.0
ENV WEBSOCKET_PORT=8765
ENV API_HOST=0.0.0.0
ENV API_PORT=8003

# Starten der Anwendung
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8003"]
