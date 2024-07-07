Dieses README bietet eine Übersicht über verschiedene Kommandozeilen Befehle, die im Rahmen dieses Projekts verwendet werden.


# 1. Docker Befehle

Hier sind einige nützliche Docker-Befehle für das Projektmanagement:

## 1.1 Allgemeine Docker Befehle

### 1.1.1 Stoppen aller Container

```bash
docker stop $(docker ps -aq)
```

### 1.1.2 Löschen aller Container

```bash
docker rm $(docker ps -aq)
```

### 1.1.3 Löschen aller Images

```bash
docker rmi $(docker images -q)
```

#### 1.1.3.1 Löschen eines einzelnen Images

Ersetze `[Image-ID]` mit der entsprechenden Image-ID:

```bash
docker rmi [Image-ID]
```

### 1.1.4 Starten eines gestoppten Containers

Ersetze `[Container-ID]` mit der entsprechenden Container-ID:

```bash
docker start [Container-ID]
```

### 1.1.5 Anzeigen aller laufenden Container

```bash
docker ps
```

#### 1.1.5.1 Anzeigen aller Container (egal ob laufend oder gestoppt)

```bash
docker ps -a
```

### 1.1.6 Starten von Docker Compose

```bash
docker compose up -d
```

### 1.1.7 Beenden von Docker Compose und Löschen von Volumes

```bash
docker-compose down -v
```
## 1.2 Datenbank-Operationen in Docker

Überprüfe und interagiere mit der Datenbank im Docker-Container mit folgenden Befehlen:

### 1.2.2 Zugriff auf den Container via Bash

Ersetze `[Container-ID oder Name]` mit der entsprechenden ID oder dem Namen des Containers (sieht man durch docker ps oder docker ps -a):

```bash
docker exec -it [Container-ID oder Name] bash
```

### 1.2.3 Verbinden mit der PostgreSQL-Datenbank (im Docker Container)

```bash
psql -U [User] -d [Datenbankname] (In unserem Fall: psql -U user -d meine_db)
```

### 1.2.4 Anzeigen aller Tabellen

```bash
\d
```

### 1.2.5 Ausführen von SQL-Abfragen

Beispielabfragen:

```sql
SELECT * FROM accounts;
SELECT id, account_id, description, created_at FROM posts;
```

# 2. Lokale zusatz Befehle

### 2.1 Erstellen von `requirements.txt` aus einer Conda-Umgebung

Um die `requirements.txt` automatisch aus der Conda-Umgebung zu erstellen, verwende den folgenden Befehl:

```bash
conda list -e > requirements.txt
```

## 2.2 Lokaler Start der API ohne Docker

```bash
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

## 2.1 Frontend starten

Navigiere ins Frontend-Verzeichnis. Beim ersten Mal führe `npm i` aus, danach `npm run dev`.



