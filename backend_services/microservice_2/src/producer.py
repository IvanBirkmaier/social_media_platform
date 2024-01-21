from confluent_kafka import Producer
import os
import logging

logging.basicConfig(level=logging.INFO)

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')


producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})

def delivery_report(err, msg):
    if err is not None:
        logging.error(f'### KAFKA PRODUCER MICROSERVICE 1: Nachrichtenübermittlung fehlgeschlagen: {err}')
    else:
        logging.info(f'### KAFKA PRODUCER MICROSERVICE 1: Nachricht erfolgreich gesendet: {msg.topic()} [{msg.partition()}]')

def kafka_send_post_id(post_id):
    producer.produce(KAFKA_TOPIC, key='post_id', value=str(post_id), callback=delivery_report)
    producer.flush()

