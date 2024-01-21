import logging
from .model import Post
from .optimizer import compress_image_bytes, resize_image
from sqlalchemy.orm import Session
from PIL import Image
import io

# # Konfigurieren des Loggings
# logging.basicConfig(level=logging.INFO)

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

def optimize_and_update_image(db: Session, post_id: int, target_width: int = 640, target_height: int = 480):
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            logging.warning(f"Post mit ID {post_id} nicht gefunden.")
            return False

        if not post.full_image:
            logging.info(f"Kein Bild zum Optimieren für Post ID {post_id} vorhanden.")
            return True

        optimized_image_bytes = compress_image_bytes(post.full_image)
        post.full_image = optimized_image_bytes
        logging.info(f"DATENTYP ÄNDER: Bild für Post ID {post_id} erfolgreich optimiert.")

        # resized_image_bytes = scale_down()
        resized_image_bytes = resize_image(optimized_image_bytes, target_width, target_height)
        post.reduced_image = resized_image_bytes
        logging.info(f"BILD QUALITÄT REDUZIEREN: Bild für Post ID {post_id} erfolgreich reduziert.")

        db.commit()
        print("Post erfolgreich aktualisiert mit dem verkleinerten Bild")
        return True

    except Exception as e:
        logging.error(f"Fehler bei der Bildoptimierung für Post ID {post_id}: {e}", exc_info=True)
        return False
    

# def resize_and_save_image(db: Session, post_id: int, target_width: int = 640, target_height: int = 480):
#     try:
#         post = db.query(Post).filter(Post.id == post_id).first()
#         if not post:
#             logging.warning(f"Post mit ID {post_id} nicht gefunden.")
#             return False

#         if not post.full_image:
#             logging.info(f"Kein Bild zum Verkleinern für Post ID {post_id} vorhanden.")
#             return True

#         resized_image_bytes = 
#         post.reduced_image = resized_image_bytes
#         logging.info(f"BILD VERKLEINERN: Bild für Post ID {post_id} auf {target_width}x{target_height} erfolgreich verkleinert.")

#         db.commit()
#         return True

#     except Exception as e:
#         logging.error(f"Fehler bei der Bildverkleinerung für Post ID {post_id}: {e}", exc_info=True)
#         return False
