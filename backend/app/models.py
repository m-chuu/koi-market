from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Product(Base):
    """SQLAlchemy model for Koi fish products."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name_en = Column(String(100), nullable=False, index=True)
    name_cn = Column(String(100), nullable=False)
    size_range = Column(String(20), nullable=False)
    price_min = Column(Numeric(10, 2), nullable=False)
    price_max = Column(Numeric(10, 2), nullable=False)
    image_path = Column(String(255), nullable=True)
    currency = Column(String(10), default="RM")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Product(id={self.id}, name_en='{self.name_en}', name_cn='{self.name_cn}')>"
