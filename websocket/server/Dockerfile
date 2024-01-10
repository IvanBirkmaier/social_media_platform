# Verwenden eines offiziellen Python-Images als Basis
FROM python:3.9-slim

# Setzen des Arbeitsverzeichnisses im Container
WORKDIR /app

# Kopieren der Anforderungsdatei in das Arbeitsverzeichnis
COPY requirements.txt .

# Installieren der benötigten Python-Pakete
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren des WebSocket-Server-Skripts in das Arbeitsverzeichnis
COPY websocket_server.py .

# Setzen von Umgebungsvariablen
ENV WEBSOCKET_SERVER_HOST=0.0.0.0
ENV WEBSOCKET_SERVER_PORT=8765

# Öffnen des Ports, auf dem der Server laufen wird
EXPOSE 8765

# Starten des WebSocket-Servers
CMD ["python", "websocket_server.py"]
