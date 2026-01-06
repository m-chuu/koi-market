from pydantic import BaseModel

# Base schema (shared properties)
class KoiBase(BaseModel):
    name: str
    price: float
    category: str
    image: str
    description: str

# Schema for creating a koi (Client -> Server)
class KoiCreate(KoiBase):
    pass

# Schema for reading a koi (Server -> Client)
class Koi(KoiBase):
    id: int

    class Config:
        from_attributes = True # Allows Pydantic to read SQLAlchemy models