from sqlalchemy import Column, Integer, ForeignKey, Text, LargeBinary, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv


load_dotenv() 
# DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASE_URL = "postgresql://user:password@db:5432/meine_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



Base = declarative_base()

# Post-Modell für Beiträge
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    description = Column(Text)
    image = Column(LargeBinary)
    created_at = Column(DateTime, default=datetime.utcnow)
