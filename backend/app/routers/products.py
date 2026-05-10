from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models import Product
from app.schemas import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse,
)

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=ProductListResponse)
def get_products(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by name"),
    db: Session = Depends(get_db),
):
    """Get all products with pagination and optional search."""
    query = db.query(Product)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Product.name_en.ilike(search_term)) | (Product.name_cn.ilike(search_term))
        )

    total = query.count()
    offset = (page - 1) * page_size
    products = query.offset(offset).limit(page_size).all()

    return ProductListResponse(
        products=[ProductResponse.from_db_model(p) for p in products],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a single product by ID."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse.from_db_model(product)


@router.post("", response_model=ProductResponse, status_code=201)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product."""
    db_product = Product(
        name_en=product_data.name_en,
        name_cn=product_data.name_cn,
        size_range=product_data.size_range,
        price_min=product_data.price.min,
        price_max=product_data.price.max,
        image_path=product_data.image_path,
        currency=product_data.currency,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return ProductResponse.from_db_model(db_product)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)
):
    """Update an existing product."""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product_data.model_dump(exclude_unset=True, by_alias=False)

    if "price" in update_data and update_data["price"]:
        db_product.price_min = update_data["price"]["min"]
        db_product.price_max = update_data["price"]["max"]
        del update_data["price"]

    for field, value in update_data.items():
        if value is not None:
            setattr(db_product, field, value)

    db.commit()
    db.refresh(db_product)
    return ProductResponse.from_db_model(db_product)


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product."""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()
    return None
