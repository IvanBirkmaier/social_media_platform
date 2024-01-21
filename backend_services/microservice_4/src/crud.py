from sqlalchemy.orm import Session
from .model import Profile
import logging

logging.basicConfig(level=logging.INFO)


# Erstellen eines Profils
def create_profile(db: Session, account_id: int, vorname: str, nachname: str, city: str, plz: int, street: str, phone_number: str):
    profile = Profile(account_id=account_id, vorname=vorname, nachname=nachname, city=city, plz=plz, street=street, phone_number=phone_number)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

# Lesen eines Profils über die Account-ID
def read_profile(db: Session, account_id: int):
    return db.query(Profile).filter(Profile.account_id == account_id).first()




