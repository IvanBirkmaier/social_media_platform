import logging
from .model import Post
from .optimizer import compress_image_bytes
from sqlalchemy.orm import Session

# Konfigurieren des Loggings
logging.basicConfig(level=logging.INFO)

def optimize_and_update_image(db: Session, post_id: int):
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            logging.warning(f"Post mit ID {post_id} nicht gefunden.")
            return False

        if not post.image:
            logging.info(f"Kein Bild zum Optimieren für Post ID {post_id} vorhanden.")
            return True

        optimized_image_bytes = compress_image_bytes(post.image)
        post.image = optimized_image_bytes
        db.commit()
        logging.info(f"Bild für Post ID {post_id} erfolgreich optimiert.")
        return True

    except Exception as e:
        logging.error(f"Fehler bei der Bildoptimierung für Post ID {post_id}: {e}", exc_info=True)
        return False
