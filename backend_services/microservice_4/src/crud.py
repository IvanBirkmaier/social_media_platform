from sqlalchemy.orm import Session
from .model import Account, Comment
from .producer import kafka_send_comment_id
import logging

logging.basicConfig(level=logging.INFO)


# Erstellen eines Kommentars
def create_comment(db: Session, account_id: int, post_id: int, text: str):
    db_comment = Comment(account_id=account_id, post_id=post_id, text=text)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    
    # Senden der Kommentar-ID an Kafka
    kafka_send_comment_id(db_comment.id)
    logging.info(f"##KAFKA: COMMENT ID {db_comment.id} erfolgreich an Server gesendet...")

    return db_comment

def get_post_comments(db: Session, post_id: int):
    comments_with_username = (
        db.query(Comment, Account.username)
        .join(Account, Comment.account_id == Account.id)
        .filter(Comment.post_id == post_id)
        .order_by(Comment.created_at.desc())
        .all()
    )

    return [
        {
            "comment_id": comment.id,
            "account_id": comment.account_id,
            "text": comment.text,
            "created_at": comment.created_at,
            "username": username,
            "classifier": comment.classifier
        }
        for comment, username in comments_with_username
    ]





