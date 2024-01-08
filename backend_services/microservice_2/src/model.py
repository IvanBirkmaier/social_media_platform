from sqlalchemy import Column, Integer, String, ForeignKey, Text, LargeBinary, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@db:5432/meine_db')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Profil-Modell
class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), unique=True)
    vorname = Column(String)
    nachname = Column(String)
    city = Column(String)
    plz = Column(Integer)
    street = Column(String)
    phone_number = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# Account-Modell
class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("Profile", back_populates="account", uselist=False)
    posts = relationship("Post", back_populates="account")
    comments = relationship("Comment", back_populates="account")

# Post-Modell
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    description = Column(Text)
    image = Column(LargeBinary)
    created_at = Column(DateTime, default=datetime.utcnow)

    account = relationship("Account", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

# Comment-Modell
class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    text = Column(Text)
    classifier = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    account = relationship("Account", back_populates="comments")
    post = relationship("Post", back_populates="comments")

# Definieren der bidirektionalen Beziehungen
Profile.account = relationship("Account", back_populates="profile")
Account.profile = relationship("Profile", back_populates="account")
Account.posts = relationship("Post", back_populates="account")
Account.comments = relationship("Comment", back_populates="account")
Post.account = relationship("Account", back_populates="posts")
Post.comments = relationship("Comment", back_populates="post")
Comment.account = relationship("Account", back_populates="comments")
Comment.post = relationship("Post", back_populates="comments")
