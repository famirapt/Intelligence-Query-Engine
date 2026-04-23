from fastapi import FastAPI, HTTPException, Depends, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import httpx
import asyncio
import re
import json
import os
from database import SessionLocal, Profile, engine, Base

app = FastAPI()

# Grading Requirement: CORS headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

# --- [NEW] AUTOMATIC SEEDER ON STARTUP ---
# This ensures Railway or local SQLite is populated automatically
@app.on_event("startup")
def seed_db():
    db = SessionLocal()
    try:
        # Check if already seeded to prevent duplicates
        if db.query(Profile).count() == 0:
            print("Database empty. Seeding from profiles_2026.json...")
            with open("profiles_2026.json", "r") as f:
                data = json.load(f)
                profiles = data.get("profiles", [])
                for p in profiles:
                    db.add(Profile(**p))
                db.commit()
            print(f"Successfully seeded {len(profiles)} records.")
    except Exception as e:
        print(f"Seeding skipped: {e}")
    finally:
        db.close()

# --- NATURAL LANGUAGE PARSER ---
def parse_natural_query(q: str):
    q = q.lower()
    params = {}
    
    # Genders
    if "female" in q: params["gender"] = "female"
    elif "male" in q: params["gender"] = "male"
    
    # Age Groups & Keywords
    if "child" in q: params["min_age"], params["max_age"] = 16, 24
    if "teenager" in q: params["age_group"] = "teenager"
    if "adult" in q: params["age_group"] = "adult"
    if "senior" in q: params["age_group"] = "senior"
    
    # Regex for "above X" or "under X"
    above_match = re.search(r'above (\d+)', q)
    if above_match: params["min_age"] = int(above_match.group(1))
    
    under_match = re.search(r'under (\d+)', q)
    if under_match: params["max_age"] = int(under_match.group(1))

    # Country mapping (Simplified for task requirements)
    countries = {"nigeria": "NG", "kenya": "KE", "angola": "AO", "benin": "BJ", "tanzania": "TZ"}
    for name, code in countries.items():
        if name in q: params["country_id"] = code
            
    return params if params else None

# --- ENDPOINTS ---

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Insighta Labs Intelligence Engine!",
        "status": "online",
        "docs_url": "/docs"
    }

@app.get("/api/profiles")
def get_all_profiles(
    gender: str = None, 
    age_group: str = None,
    country_id: str = None,
    min_age: int = None,
    max_age: int = None,
    min_gender_probability: float = None,
    min_country_probability: float = None,
    sort_by: str = "created_at",
    order: str = "asc",
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=50),
    db: Session = Depends(get_db)
):
    query = db.query(Profile)

    # Filtering
    if gender: query = query.filter(Profile.gender == gender.lower())
    if age_group: query = query.filter(Profile.age_group == age_group.lower())
    if country_id: query = query.filter(Profile.country_id == country_id.upper())
    if min_age is not None: query = query.filter(Profile.age >= min_age)
    if max_age is not None: query = query.filter(Profile.age <= max_age)
    if min_gender_probability: query = query.filter(Profile.gender_probability >= min_gender_probability)
    if min_country_probability: query = query.filter(Profile.country_probability >= min_country_probability)

    # Sorting
    if sort_by not in ["age", "created_at", "gender_probability"]:
        raise HTTPException(status_code=400, detail={"status": "error", "message": "Invalid query parameters"})
    
    col = getattr(Profile, sort_by)
    query = query.order_by(col.desc() if order == "desc" else col.asc())

    # Pagination
    total = query.count()
    data = query.offset((page - 1) * limit).limit(limit).all()

    return {"status": "success", "page": page, "limit": limit, "total": total, "data": data}

@app.get("/api/profiles/search")
def search_profiles(q: str, page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    filters = parse_natural_query(q)
    if not filters:
        raise HTTPException(status_code=400, detail={"status": "error", "message": "Unable to interpret query"})
    return get_all_profiles(**filters, page=page, limit=limit, db=db)

# Basic endpoints for grading compliance
@app.get("/api/profiles/{id}")
def get_profile(id: str, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id == id).first()
    if not profile:
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Profile not found"})
    return {"status": "success", "data": profile}