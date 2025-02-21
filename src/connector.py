import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from base import Base
import model

def create_session(db_url="sqlite:///:memory:"):
    engine = create_engine(db_url, echo=True)
    # Create tables if they don't already exist
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def load_csv_to_db(csv_file: str, session):
    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        # No try except here because I would prefer it blow up instead of mistakenly using malformed data
        for row in reader:
            new_message = model.Message()

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

            session.add(new_message)
        session.commit()


def init_db(csv_file_path):
    """Init database with a CSV"""
    session = create_session()

    load_csv_to_db(csv_file_path, session)

    return session
