1. Ports checken auf meinem PC welche sind frei welche sind belegt und vorallem mit was
2. Testen ob das Frontend  mit den Args auch läuft wenn diese nicht mehr mit Env überschreiben werden.
3. Websocket-Client checken ob das mit der Env so fnktioniert bzgl. der Übergabe der Websocket server URl

4. Frontendscript hinzufügen was Env zur laufzeit lädt nicht zur bild-zeit

Dein Problem liegt darin, dass Docker `ARG` Werte zur Build-Zeit verwendet, während `ENV` Variablen zur Laufzeit in deinem Container verfügbar sind. Wenn du dein Frontend baust, nimmst du die `ARG` Werte, um eine statische Datei zu erstellen, die deine Umgebungsvariablen enthält. Diese Dateien können nach dem Build-Prozess nicht einfach durch Umgebungsvariablen im Kubernetes-Pod überschrieben werden, da die Werte bereits in den gebauten Dateien "festgebacken" sind.

Um dieses Problem zu lösen, gibt es mehrere Ansätze:

### 1. Environment Variables zur Laufzeit
Du kannst dein Frontend so anpassen, dass es Umgebungsvariablen zur Laufzeit lädt, anstatt zur Build-Zeit. Eine gängige Methode dafür ist, ein kleines Skript zu verwenden, das beim Start des Containers ausgeführt wird und die Umgebungsvariablen in eine Konfigurationsdatei schreibt, die dann vom Frontend gelesen wird. Dies kann beispielsweise ein JavaScript-File sein, das im `public` Verzeichnis deiner App platziert wird und von deinem HTML-File eingebunden wird.

### 2. Templating Tools verwenden
Ein weiterer Ansatz wäre die Verwendung von Templating-Tools wie `envsubst`, `confd` oder `consul-template`, die es dir ermöglichen, Konfigurationsdateien zur Laufzeit aus Vorlagen und Umgebungsvariablen zu generieren. Diese Tools können als Teil deines Container-Startprozesses ausgeführt werden, um die richtigen Werte einzusetzen, bevor deine Frontend-Anwendung gestartet wird.

### 3. Kubernetes Init Containers
Du könntest auch Kubernetes Init Containers verwenden, um deine Konfigurationsdateien vor dem Start deines Frontend-Servers zu generieren oder zu modifizieren. Init Containers werden vor den regulären Containern in einem Pod ausgeführt und können dazu verwendet werden, Setup-Skripte oder andere vorbereitende Schritte durchzuführen.

### Beispiel für ein Startup-Script
Hier ein einfaches Beispiel, wie ein Startup-Skript aussehen könnte, das `envsubst` verwendet, um Umgebungsvariablen in eine Konfigurationsdatei zur Laufzeit einzusetzen:

```bash
#!/bin/sh
# Ersetzt Umgebungsvariablen in einer Vorlagendatei und speichert das Ergebnis
envsubst < /app/config.template.js > /app/config.js

# Startet den eigentlichen Frontend-Server
exec nginx -g 'daemon off;'
```

Du müsstest dann sicherstellen, dass dieses Skript beim Start deines Containers ausgeführt wird. Dies kann durch Anpassen des `CMD` oder `ENTRYPOINT` in deinem `Dockerfile` geschehen.

Wichtig ist, dass du deine Frontend-Anwendung so anpasst, dass sie Konfigurationswerte aus dieser neuen Quelle lädt, anstatt sie zur Build-Zeit fest einzucodieren.

Um dein Frontend flexibel zu halten und es dynamisch mit den verschiedenen Microservices in unterschiedlichen Umgebungen (lokal, Docker, Kubernetes) zu verbinden, kannst du folgende Strategien anwenden:

### 1. Runtime Configuration über ein externes JavaScript-File
Eine gängige Methode, um Frontend-Anwendungen flexibel zu konfigurieren, besteht darin, die Konfiguration zur Laufzeit zu laden, anstatt sie zur Build-Zeit fest einzucodieren. Du kannst ein JavaScript-File verwenden, das Konfigurationswerte aus den Umgebungsvariablen des Containers liest und sie dann deiner Anwendung zur Laufzeit zur Verfügung stellt.

#### Schritte:

- **Konfigurations-Script erstellen:** Erstelle ein JavaScript-File (z.B. `config.js`), das beim Start des Containers ausgeführt wird und die Umgebungsvariablen in eine globale Variable schreibt, die von deinem Frontend-Code verwendet werden kann.

- **Container-Startprozess anpassen:** Füge deinem Docker-Container ein Start-Skript hinzu, das dieses `config.js` File generiert, bevor die Hauptanwendung (z.B. ein Webserver wie Nginx) gestartet wird. Dieses Skript kann Tools wie `envsubst` nutzen, um Umgebungsvariablen in das JavaScript-File einzusetzen.

- **Frontend anpassen:** Ändere dein Frontend so, dass es Konfigurationswerte aus dieser neuen `config.js` Datei liest, anstatt feste URLs zu verwenden.

### 2. Einbinden des Konfigurations-Scripts in dein Frontend

- **HTML-Änderung:** Stelle sicher, dass dein `index.html` oder der Einstiegspunkt deiner Anwendung das `config.js` Skript lädt, bevor deine Haupt-JavaScript-Bundles geladen werden.

### Beispiel für ein Konfigurations-Script

```javascript
// config.js.template
window.env = {
  VITE_URL_MICROSERVICE_ONE: '${VITE_URL_MICROSERVICE_ONE}',
  VITE_URL_MICROSERVICE_TWO: '${VITE_URL_MICROSERVICE_TWO}',
  // Füge weitere URLs hier hinzu
};
```

Das Start-Skript könnte so aussehen:

```bash
#!/bin/sh
# Verwendet envsubst, um Umgebungsvariablen in config.js zu setzen
envsubst < /app/config.js.template > /app/public/config.js

# Startet den Webserver
exec nginx -g 'daemon off;'
```

### 3. Verwendung in deinem Frontend

Im Frontend-Code kannst du nun auf diese Konfiguration zugreifen, z.B.:

```javascript
const apiBaseUrl = window.env.VITE_URL_MICROSERVICE_ONE;
```

### Vorteile dieses Ansatzes

- **Flexibilität:** Du kannst die URLs deiner Microservices einfach über Umgebungsvariablen konfigurieren, ohne den Frontend-Code neu bauen zu müssen.
- **Umweltübergreifend:** Egal, ob du lokal, in einem Docker-Container oder in einem Kubernetes-Cluster arbeitest, du kannst die Umgebungsvariablen entsprechend anpassen, um die korrekten URLs zu verwenden.

Diese Methode ermöglicht es dir, deine Frontend-Anwendung flexibel und umgebungsspezifisch zu konfigurieren, indem du einfach die Umgebungsvariablen des Containers anpasst, in dem sie läuft.