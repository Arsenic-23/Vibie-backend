from sqlalchemy import Column, Integer, String, Text
from app.db.base_class import Base

class Song(Base):
    __tablename__ = "songs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    artist = Column(String)
    album = Column(String, nullable=True)
    duration = Column(Integer)  # duration in seconds
    url = Column(Text)
    queued_for = relationship("SongQueue", back_populates="song")
    streams = relationship("Stream", back_populates="current_song")
    
    def __init__(self, title: str, artist: str, album: str, duration: int, url: str):
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration
        self.url = url