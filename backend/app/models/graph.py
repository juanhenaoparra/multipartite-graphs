from sqlalchemy import Column, Integer, String
from ..config.settings import Base


class Graph(Base):
    __tablename__ = "graphs"


    name = Column(String(100),primary_key=True)
    data = Column(String(1000000), nullable=False)

