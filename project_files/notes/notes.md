### Verwendete Technologien für das Styling (Frontend):
- Tailwind
- Shadcn

### Bitte beachten bei kafka Init-Fehler (kafka/init/init.sh) 

- `init.sh` in `init` von `CRLF` auf `LS` stellen. Dass hat was damit zu tun, dass der Zeilenumbruch im Container (Linux/Ubuntu-Systeme) nicht ausgeführt werden kann. 

### Infrastrktur
Geiler Beitrag über die [Booking.com Infrastruktur](https://medium.com/@sahintalha1/high-level-system-architecture-of-booking-com-06c199003d94).
Geiler Beitrag über die [Kafka](https://blog.devgenius.io/a-practical-guide-to-build-data-streaming-from-mysql-to-elasticsearch-using-kafka-connectors-c311cf29ed38).
- ETL Prozesse mit Kafka.

### Technologien zum anschauen
1. CDN für die Handhabung von Bildern.
2. ElasticSearch als Suchmaschine geht gut mit Kafka.
3. Envoy???
4. ADN (Application Delivery Network) based on HAProxy für das Loadbalancing des Netzwerk-Traffics. 