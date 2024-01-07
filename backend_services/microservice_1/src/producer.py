from confluent_kafka import Producer
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)


load_dotenv() 
# Umgebungsvariablen laden
KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS')
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC')


def kafka_send_post_id(post_id):
    producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})
    producer.produce(KAFKA_TOPIC, key='post_id', value=str(post_id))
    producer.flush()
    logging.info(f"Post-ID {post_id} an Kafka gesendet")



## Notizen

# Eventuell Deliver Callback aufsetzen 