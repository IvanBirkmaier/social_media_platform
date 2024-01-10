# Verwenden eines offiziellen Python-Images als Basis
FROM python:3.9

# Setzen des Arbeitsverzeichnisses im Container
WORKDIR /usr/src/app

# Kopieren der Abhängigkeiten und Installieren
COPY client_1/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren des gesamten Quellcodes in das Arbeitsverzeichnis
COPY client_1/ .

# Setzen von Umgebungsvariablen
ENV WEBSOCKET_SERVER_HOST=0.0.0.0
ENV WEBSOCKET_PORT=8765
ENV API_HOST=0.0.0.0
ENV API_PORT=8003


# Exponieren des Ports, auf dem der FastAPI-Server läuft
EXPOSE 8003

# Starten der Anwendung
CMD ["python", "./app.py"]
