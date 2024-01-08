#!/bin/bash
# init.sh

# Umgebungsvariablen
KAFKA_BROKER_ADDRESS=${KAFKA_BROKER_ADDRESS:-"kafka:9092"}
KAFKA_TOPIC_ONE=${KAFKA_TOPIC_ONE:-"post_queue"}
KAFKA_TOPIC_TWO=${KAFKA_TOPIC_TWO:-"comment_queue"}
KAFKA_TOPIC_THREE=${KAFKA_TOPIC_THREE:-"classified_comments_queue"}


# Warten, bis Kafka verfügbar ist
echo "Warten auf Kafka..."
cub kafka-ready -b $KAFKA_BROKER_ADDRESS 1 20 || exit 1

# Funktion zum Erstellen eines Kafka-Topics
create_kafka_topic() {
    local topic_name=$1
    echo "Erstellen des Kafka-Topics: $topic_name"
    kafka-topics --create --if-not-exists --bootstrap-server $KAFKA_BROKER_ADDRESS --partitions 1 --replication-factor 1 --topic $topic_name
    if [ $? -ne 0 ]; then
        echo "Fehler beim Erstellen des Topics: $topic_name"
        exit 1
    fi
}

# Erstellen von Kafka-Topics
create_kafka_topic $KAFKA_TOPIC_ONE
create_kafka_topic $KAFKA_TOPIC_TWO
create_kafka_topic $KAFKA_TOPIC_THREE


echo "Kafka Topics $KAFKA_TOPIC_ONE, $KAFKA_TOPIC_TWO und $KAFKA_TOPIC_THREE erfolgreich erstellt."
