from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import datetime

class Stream(Base):
    __tablename__ = "streams"
    
    id = Column(Integer, primary_key=True, index=True)
    stream_id = Column(String, unique=True, index=True, nullable=False)
    song_id = Column(Integer, ForeignKey('songs.id'))
    current_song = relationship("Song", back_populates="streams")
    users = relationship("User", back_populates="stream")
    queue = relationship("SongQueue", back_populates="stream")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    def __init__(self, stream_id: str, song_id: int):
        self.stream_id = stream_id
        self.song_id = song_id

class SongQueue(Base):
    __tablename__ = "song_queue"
    
    id = Column(Integer, primary_key=True, index=True)
    stream_id = Column(Integer, ForeignKey('streams.id'))
    song_id = Column(Integer, ForeignKey('songs.id'))
    stream = relationship("Stream", back_populates="queue")
    song = relationship("Song", back_populates="queued_for")
    queued_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    def __init__(self, stream_id: int, song_id: int):
        self.stream_id = stream_id
        self.song_id = song_id