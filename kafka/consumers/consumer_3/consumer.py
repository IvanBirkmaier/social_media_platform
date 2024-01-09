from confluent_kafka import Consumer, KafkaError
import requests
import os
import logging
import time

logging.basicConfig(level=logging.INFO)

# Laden der Umgebungsvariablen
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'classified_comments_queue')
WEBSOCKET_CLIENT_URL = os.getenv('WEBSOCKET_CLIENT_URL', 'http://websocket-client:8003/trigger_update')


# Konfiguration des Consumers
consumer = Consumer({
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'group.id': 'classifier-group',
    'auto.offset.reset': 'earliest'
})

# Funktion, um das Kafka-Topic zu überprüfen
def check_topic_exists(topic, timeout=60):
    """ Überprüft, ob ein bestimmtes Kafka-Topic existiert. """
    start_time = time.time()
    while time.time() - start_time < timeout:
        topics = consumer.list_topics().topics
        if topic in topics:
            return True
        time.sleep(5)
    return False

# Funktion zum Senden von Klassifizierungsanfragen
def send_classification_request(comment_id):
    # Erstellen der JSON-Datenstruktur für die Anfrage
    data = {"comment_id": comment_id}
    # Senden der POST-Anfrage mit der JSON-Datenstruktur
    response = requests.post(WEBSOCKET_CLIENT_URL, json=data)
    if response.status_code == 200:
        logging.info(f"Klassifizierung erfolgreich für Kommentar ID {comment_id}")
    else:
        logging.error(f"Fehler bei der Klassifizierung für Kommentar ID {comment_id}: {response.text}")

# Warte, bis das Topic verfügbar ist
if check_topic_exists(KAFKA_TOPIC):
    logging.info(f"Kafka Topic {KAFKA_TOPIC} gefunden. Starte Consumer...")
    consumer.subscribe([KAFKA_TOPIC])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() != KafkaError._PARTITION_EOF:
                    logging.error(msg.error())
                    break
            else:
                comment_id = msg.value().decode('utf-8')
                send_classification_request(comment_id)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
else:
    logging.error(f"Kafka Topic {KAFKA_TOPIC} nicht gefunden.")
