from app.database import SessionLocal, engine
from app.models import Base, Koi

# Ensure tables exist
Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()

    # Check if data already exists to avoid duplicates
    if db.query(Koi).count() > 0:
        print("Database already contains data. Skipping seed.")
        return

    # The Mock Data you had in React
    kois = [
        Koi(
            name="Tancho Kohaku",
            category="Kohaku",
            price=1200,
            image_url="https://placehold.co/400x300/ff7b7b/white?text=Tancho+Kohaku",
            description="Pristine white body with a perfect round red spot on the head."
        ),
        Koi(
            name="Showa Sanshoku",
            category="Showa",
            price=850,
            image_url="https://placehold.co/400x300/333/white?text=Showa",
            description="Beautiful balance of red, white, and black patterns."
        ),
        Koi(
            name="Ogon Yamabuki",
            category="Ogon",
            price=2500,
            image_url="https://placehold.co/400x300/ffd700/333?text=Ogon+Gold",
            description="Solid metallic gold color. A symbol of wealth."
        )
    ]

    db.add_all(kois)
    db.commit()
    print("✅ Successfully seeded 3 Koi fish into the database!")
    db.close()

if __name__ == "__main__":
    seed_data()