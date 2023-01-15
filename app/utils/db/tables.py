from sqlalchemy import TIMESTAMP, Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Products(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String)
    slug = Column(String)
    image = Column(String)
    status = Column(String)
    description = Column(String)
    price = Column(String)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
