#!/bin/sh

# Stelle sicher, dass envsubst verfügbar ist
apk add --no-cache gettext

# Ersetze die Umgebungsvariablen im Template und speichere das Ergebnis als config.js
envsubst < /config-template.js > /usr/share/nginx/html/config.js

# Starte Nginx im Vordergrund
exec nginx -g 'daemon off;'
