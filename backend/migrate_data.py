#!/usr/bin/env python3
"""
Data Migration Script for Koi Market

Reads product data from seed_data.json and inserts it into the PostgreSQL database.
Can be run standalone or as part of the Docker setup.

Usage:
    python migrate_data.py                    # Uses DATABASE_URL from environment
    python migrate_data.py --clear            # Clear existing data before inserting
    python migrate_data.py --dry-run          # Preview without inserting
"""

import json
import os
import sys
import argparse
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from app.models import Product, Base


def get_database_url() -> str:
    """Get database URL from environment or use default."""
    return os.getenv(
        "DATABASE_URL",
        "postgresql://koiuser:koipassword@localhost:5432/koi_market"
    )


def load_seed_data(file_path: str = None) -> list[dict]:
    """Load product data from JSON file."""
    if file_path is None:
        file_path = Path(__file__).parent / "seed_data.json"

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def create_product_from_dict(data: dict) -> Product:
    """Convert JSON product data to SQLAlchemy model."""
    return Product(
        name_en=data["nameEn"],
        name_cn=data["nameCn"],
        size_range=data["sizeRange"],
        price_min=data["price"]["min"],
        price_max=data["price"]["max"],
        image_path=data.get("image"),
        currency=data.get("currency", "RM"),
    )


def migrate(
    database_url: str = None,
    clear_existing: bool = False,
    dry_run: bool = False,
    seed_file: str = None,
) -> dict:
    """
    Run the migration.

    Args:
        database_url: PostgreSQL connection string
        clear_existing: If True, delete all existing products first
        dry_run: If True, only preview changes without committing
        seed_file: Path to JSON seed file

    Returns:
        dict with migration results
    """
    if database_url is None:
        database_url = get_database_url()

    print(f"Connecting to database...")
    print(f"  URL: {database_url.replace(database_url.split(':')[2].split('@')[0], '****')}")

    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)

    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # Load seed data
    products_data = load_seed_data(seed_file)
    print(f"\nLoaded {len(products_data)} products from seed file")

    if dry_run:
        print("\n[DRY RUN] Would insert the following products:")
        for p in products_data:
            print(f"  - {p['nameEn']} ({p['nameCn']}) - {p['currency']} {p['price']['min']}-{p['price']['max']}")
        return {"status": "dry_run", "products_count": len(products_data)}

    session = Session()
    results = {"inserted": 0, "skipped": 0, "deleted": 0}

    try:
        # Clear existing data if requested
        if clear_existing:
            deleted = session.query(Product).delete()
            results["deleted"] = deleted
            print(f"\nCleared {deleted} existing products")

        # Check for existing products
        existing_ids = {p.id for p in session.query(Product.id).all()}

        # Insert products
        for product_data in products_data:
            # Skip if product with this name already exists (to avoid duplicates on re-run)
            existing = session.query(Product).filter(
                Product.name_en == product_data["nameEn"]
            ).first()

            if existing and not clear_existing:
                print(f"  Skipping existing: {product_data['nameEn']}")
                results["skipped"] += 1
                continue

            product = create_product_from_dict(product_data)
            session.add(product)
            results["inserted"] += 1
            print(f"  Inserted: {product_data['nameEn']} ({product_data['nameCn']})")

        session.commit()
        print(f"\n✓ Migration complete!")
        print(f"  Inserted: {results['inserted']}")
        print(f"  Skipped: {results['skipped']}")
        if clear_existing:
            print(f"  Deleted: {results['deleted']}")

        # Verify
        total = session.query(Product).count()
        print(f"\nTotal products in database: {total}")

        return {"status": "success", **results, "total": total}

    except Exception as e:
        session.rollback()
        print(f"\n✗ Migration failed: {e}")
        raise
    finally:
        session.close()


def main():
    parser = argparse.ArgumentParser(
        description="Migrate product data to PostgreSQL database"
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear existing products before inserting",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without committing to database",
    )
    parser.add_argument(
        "--database-url",
        type=str,
        help="PostgreSQL connection string (overrides DATABASE_URL env var)",
    )
    parser.add_argument(
        "--seed-file",
        type=str,
        help="Path to JSON seed file (default: seed_data.json)",
    )

    args = parser.parse_args()

    print("=" * 50)
    print("Koi Market Data Migration")
    print("=" * 50)

    try:
        result = migrate(
            database_url=args.database_url,
            clear_existing=args.clear,
            dry_run=args.dry_run,
            seed_file=args.seed_file,
        )
        sys.exit(0 if result["status"] in ("success", "dry_run") else 1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
