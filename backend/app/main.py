import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import products

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Koi Market API",
    description="API for Koi Fish Store - manage products and orders",
    version="1.0.0",
)

# CORS configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

if ENVIRONMENT == "development":
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ]
else:
    origins = [
        os.getenv("FRONTEND_URL", ""),
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(products.router, prefix="/api/v1")


@app.get("/")
def root():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Koi Market API"}


@app.get("/health")
def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "environment": ENVIRONMENT,
        "version": "1.0.0",
    }
