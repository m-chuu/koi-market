import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_database_url() -> str:
    """
    Build database URL supporting both local and Cloud SQL connections.

    For Cloud SQL, uses Unix socket connection via Cloud Run's built-in connector.
    Set INSTANCE_CONNECTION_NAME for Cloud SQL (e.g., project:region:instance)
    """
    # Check for direct DATABASE_URL first (local development / explicit URL)
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    # Cloud SQL configuration
    instance_connection_name = os.getenv("INSTANCE_CONNECTION_NAME")
    if instance_connection_name:
        db_user = os.getenv("DB_USER", "postgres")
        db_pass = os.getenv("DB_PASS", "")
        db_name = os.getenv("DB_NAME", "koi_market")

        # Cloud Run provides Unix socket at /cloudsql/<instance_connection_name>
        return f"postgresql://{db_user}:{db_pass}@/{db_name}?host=/cloudsql/{instance_connection_name}"

    # Fallback to local defaults
    return "postgresql://koiuser:koipassword@localhost:5432/koi_market"


DATABASE_URL = get_database_url()

# Configure engine with connection pooling suitable for Cloud Run
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=2,
    pool_timeout=30,
    pool_recycle=1800,  # Recycle connections after 30 min
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency that provides a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
