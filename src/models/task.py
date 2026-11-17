from sqlalchemy import Column, Integer, String, Text

from src.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(100), nullable=False)

    description = Column(Text, nullable=True)

    priority = Column(String(10), default="média")

    status = Column(String(20), default="pendente")

    