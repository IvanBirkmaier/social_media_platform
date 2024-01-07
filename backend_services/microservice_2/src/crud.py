from .model import Post
from .optimizer import compress_image_bytes
from sqlalchemy.orm import Session

# Funktion, um ein Bild nach ID zu optimieren und in der Datenbank zu überschreiben
def optimize_and_update_image(db: Session, post_id: int):
    try:
        # Bild nach ID auslesen
        post = db.query(Post).filter(Post.id == post_id).first()
        if post and post.image:
            # Bild optimieren
            optimized_image_bytes = compress_image_bytes(post.image)

            # Optimiertes Bild in der Datenbank überschreiben
            post.image = optimized_image_bytes
            db.commit()
    except Exception as e:
        print(f"Fehler bei der Bildoptimierung: {e}")
