from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv() 
#DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@db:5432/meine_db')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Comment-Modell für Kommentare
class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    text = Column(Text)
    classifier = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

