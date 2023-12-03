from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv() 
DATABASE_URL = os.environ.get("DATABASE_URL")


# Der Rest Ihres Codes

#DATABASE_URL = "postgresql://user:password@localhost:5432/meine_db" # Um API local ausführen zu können. Mit laufenden DB-Container 
#DATABASE_URL = "postgresql://user:password@host.docker.internal:5432/meine_db" # Um API im Container auszuführen. Vor dem builden der Images wechseln 

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

def init_db():
    Base.metadata.create_all(bind=engine)
