from sqlalchemy import Column, Integer, String, Text, Boolean

from base import Base

# Spam message
class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    spam = Column(Boolean)

    subject = Column(Text)
    body = Column(Text)