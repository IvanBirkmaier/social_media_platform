import logging
from .model import Comment
from .classifier import classifier
from sqlalchemy.orm import Session

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
        logger.info(f"Text für Kommentar ID {comment_id} erfolgreich klassifiziert.")
        print("Kommentar: ",comment.text," ID: ", comment_id, " Klasse: ", classified_text)

        return True

    except Exception as e:
        logger.error(f"Fehler beim Klassifizieren des Kommentars ID {comment_id}: {e}", exc_info=True)
        return False
