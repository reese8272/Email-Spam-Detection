import csv
import os
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the base class for ORM models
Base = declarative_base()

# Define an ORM model for the CSV data.
class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    spam = Column(Boolean)

    subject = Column(Text)
    body = Column(Text)

def create_session(db_url="sqlite:///:memory:"):
    """
    Creates a SQLAlchemy session using an in-memory SQLite database.
    """
    engine = create_engine(db_url, echo=True)
    # Create tables if they don't already exist
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def load_csv_to_db(csv_file: str, session):
    """
    Reads data from a CSV file and inserts each row as a Message into the in-memory database.
    """
    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        # No try except here because I would prefer it blow up instead of mistakenly using malformed data
        for row in reader:
            new_message = Message()

            # Get subject
            p1 = len('Subject: ') # Between this text
            p2 = row['text'].find("\r\n") # and end of first line
            new_message.subject = row['text'][p1:p2]

            # Get body
            p1 = p2 # From end of subject
            p2 = -1 # To end of string
            new_message.body = row['text'][p1:p2]

            # Get label
            new_message.spam = row['label'] == 'spam' # TODO do better lel

            # IDGAF about the other data.

            session.add(new_message)
        session.commit()


def init_db():
    session = create_session()

    # Specify the path to your CSV file
    csv_file_path = "dataset.csv"

    # Load CSV data into the database
    load_csv_to_db(csv_file_path, session)

    # Example query: Print all messages from the in-memory database.
    return session

if __name__ == "__main__":
    session = init_db()

    # Example query: Print all messages from the in-memory database.
    messages = session.query(Message).all()
    print("\n\n\n\n")
    print(messages[0].body)
    # for message in messages:
    #     print(f"ID: {message.id}, Label: {message.label}, Label Num: {message.label_num}")
    #     print(f"Text: {message.text}\n")
