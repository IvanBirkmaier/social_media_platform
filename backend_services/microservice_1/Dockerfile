# Verwenden Sie das offizielle Python-Image als Basis
FROM python:3.9

# Setzen Sie das Arbeitsverzeichnis im Container
WORKDIR /code

# Setzen Sie Umgebungsvariablen
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# ENV DATABASE_URL=postgresql://user:password@host.docker.internal:5432/meine_db
ENV DATABASE_URL=postgresql://user:password@localhost:5432/meine_db
ENV FRONTEND_URL=http://localhost:3000


# Installieren Sie die Abhängigkeiten
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt


# Kopieren Sie den Quellcode in den Container
COPY ./src /code/src
COPY app.py /code/

# Legen Sie den Befehl fest, um die Anwendung auszuführen
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]

# Legen Sie den Port fest, auf dem die Anwendung laufen soll
EXPOSE 8001
