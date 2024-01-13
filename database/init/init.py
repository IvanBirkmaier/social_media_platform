from model import Base, engine

def create_tables():
    print("lauft")
    Base.metadata.create_all(bind=engine)
    print("beendet")

if __name__ == "__main__":
    create_tables()