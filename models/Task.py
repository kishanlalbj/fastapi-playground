from db import Base
from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP, func


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    completed = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP(timezone=True),  server_default=func.now())
