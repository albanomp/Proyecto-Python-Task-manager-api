from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id =Column(Integer, primary_key=True,index=True)
    title = Column(String(200),nullable=False )
    description = Column(Text,nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Relacion con User:
    owner = relationship("User",back_populates="projects")
# Relacion con Task:
    task = relationship("Task", back_populates="projects",cascade="all, delete-orphan")
    