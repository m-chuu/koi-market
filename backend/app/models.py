from sqlalchemy import Column, Integer, String, Float, Text
from .database import Base

class Koi(Base):
    __tablename__ = "kois"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    category = Column(String)
    image_url = Column(String) # Storing URL as text
    description = Column(Text)