from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=False)
    username = Column(String, nullable=True)
    stream_id = Column(Integer, ForeignKey('streams.id'), nullable=True)
    stream = relationship("Stream", back_populates="users")
    
    def __init__(self, telegram_id: int, name: str, username: str = None, stream_id: int = None):
        self.telegram_id = telegram_id
        self.name = name
        self.username = username
        self.stream_id = stream_id