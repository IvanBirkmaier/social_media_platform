# Verwenden Sie Alpine Linux als Basis-Image
FROM alpine:latest

# Aktualisieren Sie die Paketliste, installieren Sie Python und pip
RUN apk update && apk add python3 py3-pip

# Installieren Sie SQLite
RUN apk add sqlite

# Installieren Sie sqlite-web
RUN pip3 install sqlite-web

# Setzen Sie das Arbeitsverzeichnis
WORKDIR /sqlite

# Expose Port 8080 für sqlite-web
EXPOSE 8080

# Setzen Sie das Standardkommando, um sqlite-web zu starten
CMD ["sqlite-web", "/sqlite/mydb.sqlite", "--host", "0.0.0.0", "--port", "8080"]
