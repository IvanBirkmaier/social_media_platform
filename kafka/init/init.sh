#!/bin/bash
# init.sh

# Umgebungsvariablen
KAFKA_BROKER_ADDRESS=${KAFKA_BROKER_ADDRESS:-"kafka:9092"}
KAFKA_TOPIC=${KAFKA_TOPIC:-"post_queue"}

# Warten, bis Kafka verfügbar ist (Anpassen für Confluent Image)
echo "Warten auf Kafka..."
cub kafka-ready -b $KAFKA_BROKER_ADDRESS 1 20

# Erstellen von Kafka-Topics
kafka-topics --create --bootstrap-server $KAFKA_BROKER_ADDRESS --partitions 1 --replication-factor 1 --topic $KAFKA_TOPIC

echo "Kafka Topic $KAFKA_TOPIC erstellt."
