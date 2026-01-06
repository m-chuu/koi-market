from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database

router = APIRouter(
    prefix="/kois",
    tags=["kois"]
)

# GET all Kois
@router.get("/", response_model=List[schemas.Koi])
def read_kois(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    kois = db.query(models.Koi).offset(skip).limit(limit).all()
    return kois

# POST (Create) a new Koi
@router.post("/", response_model=schemas.Koi)
def create_koi(koi: schemas.KoiCreate, db: Session = Depends(database.get_db)):
    db_koi = models.Koi(**koi.dict())
    db.add(db_koi)
    db.commit()
    db.refresh(db_koi)
    return db_koi