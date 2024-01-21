from confluent_kafka import Producer
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv() 
KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS')
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC')

producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})

def delivery_report(err, msg):
    if err is not None:
        logging.error(f'### KAFKA PRODUCER MICROSERVICE 1: Nachrichtenübermittlung fehlgeschlagen: {err}')
    else:
        logging.info(f'### KAFKA PRODUCER MICROSERVICE 1: Nachricht erfolgreich gesendet: {msg.topic()} [{msg.partition()}]')

def kafka_send_comment_id(comment_id):
    producer.produce(KAFKA_TOPIC, key='comment_id', value=str(comment_id), callback=delivery_report)
    producer.flush()
