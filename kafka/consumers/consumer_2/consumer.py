from confluent_kafka import Consumer, KafkaError
import requests
import os
import logging
import time

logging.basicConfig(level=logging.INFO)

# Laden der Umgebungsvariablen
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'comment_queue')
MICROSERVICE_3_API_URL = os.getenv('MICROSERVICE_3_API_URL', 'http://microservice_three:8002/classify/')

# Konfiguration des Consumers
consumer = Consumer({
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'group.id': 'comment-group',
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
    response = requests.post(f"{MICROSERVICE_3_API_URL}{comment_id}")
    if response.status_code == 200:
        logging.info(f"### KAFKA CONSUMER FÜR TOPIC {KAFKA_TOPIC}: Klassifizierung erfolgreich für Kommentar ID {comment_id}")
    else:
        logging.error(f"### KAFKA CONSUMER FÜR TOPIC {KAFKA_TOPIC}: Fehler bei der Klassifizierung für Kommentar ID {comment_id}: {response.text}")

# Warte, bis das Topic verfügbar ist
if check_topic_exists(KAFKA_TOPIC):
    logging.info(f"### KAFKA CONSUMER FÜR TOPIC {KAFKA_TOPIC}: Kafka Topic {KAFKA_TOPIC} gefunden. Starte Consumer...")
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
    logging.error(f"### KAFKA CONSUMER FÜR TOPIC {KAFKA_TOPIC}: Kafka Topic {KAFKA_TOPIC} nicht gefunden.")
