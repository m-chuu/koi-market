from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import kois

# Create database tables automatically on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow Frontend (running on localhost:5173 or similar) to talk to Backend
origins = [
    "http://localhost:5173", 
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routes
app.include_router(kois.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Koi Market API"}