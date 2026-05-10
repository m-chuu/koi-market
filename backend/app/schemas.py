from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal


class PriceRange(BaseModel):
    """Nested price object matching frontend structure."""
    min: Decimal = Field(..., ge=0, description="Minimum price")
    max: Decimal = Field(..., ge=0, description="Maximum price")


class ProductBase(BaseModel):
    """Base schema with common product fields."""
    name_en: str = Field(..., min_length=1, max_length=100, alias="nameEn")
    name_cn: str = Field(..., min_length=1, max_length=100, alias="nameCn")
    size_range: str = Field(..., min_length=1, max_length=20, alias="sizeRange")
    price: PriceRange
    image_path: Optional[str] = Field(None, max_length=255, alias="image")
    currency: str = Field(default="RM", max_length=10)


class ProductCreate(ProductBase):
    """Schema for creating a new product."""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating a product (all fields optional)."""
    name_en: Optional[str] = Field(None, min_length=1, max_length=100, alias="nameEn")
    name_cn: Optional[str] = Field(None, min_length=1, max_length=100, alias="nameCn")
    size_range: Optional[str] = Field(None, min_length=1, max_length=20, alias="sizeRange")
    price: Optional[PriceRange] = None
    image_path: Optional[str] = Field(None, max_length=255, alias="image")
    currency: Optional[str] = Field(None, max_length=10)


class ProductResponse(BaseModel):
    """Schema for product responses (matches frontend structure)."""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    name_en: str = Field(..., alias="nameEn", serialization_alias="nameEn")
    name_cn: str = Field(..., alias="nameCn", serialization_alias="nameCn")
    size_range: str = Field(..., alias="sizeRange", serialization_alias="sizeRange")
    price: PriceRange
    image_path: Optional[str] = Field(None, alias="image", serialization_alias="image")
    currency: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_db_model(cls, db_product):
        """Convert SQLAlchemy model to response schema."""
        return cls(
            id=db_product.id,
            nameEn=db_product.name_en,
            nameCn=db_product.name_cn,
            sizeRange=db_product.size_range,
            price=PriceRange(min=db_product.price_min, max=db_product.price_max),
            image=db_product.image_path,
            currency=db_product.currency,
            created_at=db_product.created_at,
            updated_at=db_product.updated_at,
        )


class ProductListResponse(BaseModel):
    """Schema for paginated product list."""
    products: list[ProductResponse]
    total: int
    page: int
    page_size: int
