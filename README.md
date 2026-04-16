
---

### **README.md**

# Profile Classification & Persistence API

A high-performance FastAPI service that integrates multiple external APIs to classify names based on gender, age, and nationality. This system implements data persistence, idempotency handling, and complex filtering logic as part of the HNG Backend Stage 1 Assessment.

## 🚀 Features

* **Multi-API Integration:** Concurrently fetches data from Genderize, Agify, and Nationalize.
* **Data Classification:** Categorizes profiles into age groups (`child`, `teenager`, `adult`, `senior`).
* **Persistence:** Stores processed data in a PostgreSQL database (with SQLite support for local testing).
* **Idempotency:** Prevents duplicate records for the same name; returns existing data if available.
* **UUID v7:** Uses time-ordered UUIDs for primary keys to ensure database efficiency.
* **CORS Enabled:** Configured for cross-origin requests (`*`) to facilitate automated grading.

---

## 🛠️ Tech Stack

* **Language:** Python 3.12
* **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
* **Database:** PostgreSQL (Production) / SQLite (Local)
* **ORM:** SQLAlchemy
* **Async HTTP:** HTTPX

---

## 🏁 Getting Started

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file or set environment variables in your deployment platform:
* `DATABASE_URL`: Your PostgreSQL connection string (defaults to local SQLite if not provided).

### 3. Running Locally
```bash
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`. You can view the interactive documentation at `/docs`.

---

## 📡 API Endpoints

### **1. Create Profile**
`POST /api/profiles`
* **Body:** `{"name": "ella"}`
* **Behavior:** Fetches data, applies logic, and saves. Returns existing record if name already exists.

### **2. Get Single Profile**
`GET /api/profiles/{id}`
* **Response:** Detailed JSON of the stored profile.

### **3. Get All Profiles (with Filtering)**
`GET /api/profiles`
* **Optional Query Params:** `gender`, `country_id`, `age_group` (Case-insensitive).
* **Example:** `/api/profiles?gender=female&country_id=US`

### **4. Delete Profile**
`DELETE /api/profiles/{id}`
* **Response:** `204 No Content`.

---

## 🧪 Error Handling
The API adheres to strict error formatting:
* `400 Bad Request`: Missing/invalid name.
* `404 Not Found`: ID does not exist.
* `502 Bad Gateway`: Upstream API (Agify/Genderize/Nationalize) returned invalid data.

---

## 📄 License
This project is for educational purposes as part of the HNG Internship.

---