from model import Base, engine
import logging

logging.basicConfig(level=logging.INFO)

def create_tables():
    logging.info(f'Database initialization: Started...')
    Base.metadata.create_all(bind=engine)
    logging.info(f'Database initialization: Finished...')


if __name__ == "__main__":
    create_tables()
    logging.info(f'Database initialization: Stopped...')
