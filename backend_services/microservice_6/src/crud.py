import logging
from .model import Comment
from .classifier import classifier
from sqlalchemy.orm import Session
from .producer import kafka_send_comment_id
from dotenv import load_dotenv
import os




load_dotenv() 
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC')

# Konfigurieren des Loggings
# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Rest Ihres Codes...


def classify_comments(db: Session, comment_id: int):
    try:
        # Kommentar nach ID auslesen
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        # Überprüfen, ob der Kommentar gefunden wurde
        if not comment:
            logger.warning(f"Kommentar mit ID {comment_id} nicht gefunden.")
            return False
        # Überprüfen, ob der Kommentar Text enthält
        if not comment.text:
            logger.info(f"Kein Text zum Klassifizieren für Kommentar ID {comment_id} vorhanden.")
            return True

        # Klassifizieren des Textes
        classified_text = classifier(comment.text)

        comment.classifier = classified_text
        db.commit()
        logger.info(f"ERGEBNISS:\nKommentar: {comment.text}\nID:{comment_id}\nKlasse: {classified_text}")
        logger.info(f"OPTIMIZER: Text für Kommentar ID {comment_id} erfolgreich klassifiziert.")
        kafka_send_comment_id(comment_id)
        logger.info(f"KAFKA: Kommentar ID {comment_id} erfolgreich an Kafka-Queue: {KAFKA_TOPIC} gesendet.")

        return True

    except Exception as e:
        logger.error(f"Fehler beim Klassifizieren des Kommentars ID {comment_id}: {e}", exc_info=True)
        return False
