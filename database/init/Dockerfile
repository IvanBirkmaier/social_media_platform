# Verwenden eines offiziellen Python-Runtime als Eltern-Image
FROM python:3.9-slim

# Arbeitsverzeichnis im Container festlegen
WORKDIR /usr/src/app

# Installieren von Python-Abhängigkeiten
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren des aktuellen Verzeichnisses in das Arbeitsverzeichnis im Container
COPY . .

# Festlegen der Umgebungsvariablen
# ENV DATABASE_URL=postgresql://user:password@host.docker.internal:5432/meine_db
ENV DATABASE_URL=postgresql://user:password@localhost:5432/meine_db
      


# Befehl zum Ausführen der Anwendung
CMD ["python", "./init.py"]
