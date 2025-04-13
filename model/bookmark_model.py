from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from model import Base

class Bookmark(Base):
    __tablename__ = 'bookmarks'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    url = Column(String(500), nullable=False)
    icon_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'icon_url': self.icon_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }