from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Page(Base):
    __tablename__ = "page"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String)


class Similarity(Base):
    __tablename__ = "similarity"

    id = Column(Integer, primary_key=True)
    first = Column(Integer, ForeignKey(Page.id), nullable=False)
    second = Column(Integer, ForeignKey(Page.id), nullable=False)
    similarity = Column(Float)
