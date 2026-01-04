from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 1. Allow React to talk to this backend (CORS)
origins = ["http://localhost:5173", "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],    
    allow_headers=["*"],
)

# 2. Define what a "Koi Fish" looks like (Data Model)
class KoiFish(BaseModel):
    id: int
    name: str
    variety: str # e.g., Kohaku, Sanke
    price_myr: float
    image_url: str

# 3. Mock Database (We will replace this with PostgreSQL in Step 3)
fake_db = [
    {"id": 1, "name": "Champion Kohaku", "variety": "Kohaku", "price_myr": 1500.00, "image_url": "https://via.placeholder.com/150"},
    {"id": 2, "name": "Little Showa", "variety": "Showa", "price_myr": 350.50, "image_url": "https://via.placeholder.com/150"}
]

# 4. API Endpoints
@app.get("/")
def read_root():
    return {"message": "Welcome to the Koi Shop API"}

@app.get("/fish", response_model=List[KoiFish])
def get_fish():
    return fake_db