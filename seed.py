import json
from database import SessionLocal, Profile, engine, Base

def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        with open("profiles_2026.json", "r") as f:
            data = json.load(f)
            
        # Access the list inside the "profiles" key
        profiles_list = data.get("profiles", [])
        
        for item in profiles_list:
            exists = db.query(Profile).filter(Profile.name == item['name']).first()
            if not exists:
                db.add(Profile(**item))
        
        db.commit()
        print(f"✅ Successfully seeded {len(profiles_list)} profiles!")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()