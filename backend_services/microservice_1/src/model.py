from sqlalchemy import Column, Integer, String, ForeignKey, Text, LargeBinary, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv() 
# DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASE_URL = "postgresql://user:password@db:5432/meine_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Account-Modell für Authentifizierungsdetails
class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 1-zu-1-Beziehung zum Profil
    profile = relationship("Profile", back_populates="account", uselist=False)
    
    # 1-zu-viele-Beziehung zu Posts und Kommentaren
    posts = relationship("Post", backref="author")
    comments = relationship("Comment", backref="commenter")

# Profil-Modell für persönliche Benutzerinformationen
class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), unique=True)
    vorname = Column(String)
    nachname = Column(String)
    city = Column(String)
    plz = Column(Integer)
    street = Column(String)  # Sollte ein String sein, wenn es Straßennamen enthält
    phone_number = Column(String)  # Sollte ein String sein, um verschiedene Telefonnummern-Formate zu unterstützen
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Referenz zum Account
    account = relationship("Account", back_populates="profile")

# Post-Modell für Beiträge
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    description = Column(Text)
    image = Column(LargeBinary)
    created_at = Column(DateTime, default=datetime.utcnow)

# Comment-Modell für Kommentare
class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
