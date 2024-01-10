from confluent_kafka import Consumer, KafkaError, TopicPartition
import requests
from dotenv import load_dotenv
import os
import time
import logging

logging.basicConfig(level=logging.INFO)

# Umgebungsvariablen
load_dotenv() 
KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS')
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC')
MICROSERVICE_2_API_URL = os.environ.get('MICROSERVICE_2_API_URL')

consumer = Consumer({
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'group.id': 'post-group',
    'auto.offset.reset': 'earliest'
})

def check_topic_exists(consumer, topic, timeout=30):
    """ Prüft, ob ein bestimmtes Topic existiert. """
    start_time = time.time()
    while time.time() - start_time < timeout:
        metadata = consumer.list_topics(timeout=10)
        if topic in metadata.topics:
            return True
        time.sleep(2)
    return False

def send_optimization_request(post_id):
    response = requests.post(f"{MICROSERVICE_2_API_URL}{post_id}")
    if response.status_code == 200:
        logging.info(f"Bildoptimierung erfolgreich für Post ID {post_id}")
    else:
        logging.error(f"Fehler bei der Bildoptimierung für Post ID {post_id}: {response.text}")

if check_topic_exists(consumer, KAFKA_TOPIC):
    logging.info(f"Kafka Topic {KAFKA_TOPIC} gefunden. Starte Consumer...")
    consumer.subscribe([KAFKA_TOPIC])

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    logging.error(msg.error())
                    break

            post_id = msg.value().decode('utf-8')
            logging.info(f"Empfange Post-ID {post_id} vom Kafka")
            send_optimization_request(post_id)

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
else:
    logging.error(f"Kafka Topic {KAFKA_TOPIC} nicht gefunden.")
