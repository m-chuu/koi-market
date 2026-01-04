from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow React to talk to this backend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # This is where React runs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This is your "Database" for now (A simple list)
# You will edit this list directly to add new Koi fish.
koi_database = [
    {
        "id": 1,
        "name": "Showa Sanshoku",
        "price": "RM 450",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Showa_Sanshoku.jpg/440px-Showa_Sanshoku.jpg",
        "description": "Beautiful black body with red and white patterns."
    },
    {
        "id": 2,
        "name": "Kohaku",
        "price": "RM 300",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Kohaku_2.jpg/440px-Kohaku_2.jpg",
        "description": "Classic white body with red markings."
    }
]

@app.get("/")
def read_root():
    return {"message": "Welcome to the Koi API"}

# This endpoint sends the fish data to the frontend
@app.get("/fish")
def get_fish():
    return koi_database