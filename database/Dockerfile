FROM postgres:latest

# Umgebungsvariablen setzen
ENV POSTGRES_DB=meine_db
ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=password

# Standardport freigeben
EXPOSE 5432

# Das Datenverzeichnis als Volumen definieren
VOLUME ["/var/lib/postgresql/data"]
