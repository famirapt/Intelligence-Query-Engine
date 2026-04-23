
### README.md

```markdown
# Insighta Labs: Intelligence Query Engine

A production-grade Demographic Intelligence API built with FastAPI. This system serves as a high-performance query engine capable of segmenting large datasets through advanced filtering and rule-based Natural Language Processing.

## 🚀 Features

* **Advanced Filtering Engine:** Supports combined complex queries (gender, age ranges, country IDs, and probability thresholds).
* **Natural Language Query (NLQ):** A custom, non-AI parser that interprets plain English queries like *"young males from nigeria"* or *"females above 30"*.
* **Optimized Pagination & Sorting:** Efficiently handles the 2026 record dataset using SQL-level pagination (`limit`, `offset`) and dynamic sorting.
* **UUID v7 Integration:** Uses time-ordered UUIDs for primary keys to ensure optimal database indexing performance.
* **Automatic Data Seeding:** System automatically detects an empty database on startup and seeds it with the required 2026 demographic profiles.
* **Environment Aware:** Automatically switches between local SQLite for development and PostgreSQL for production (Railway).

## 🛠️ Tech Stack

* **Framework:** FastAPI
* **Database:** PostgreSQL (Production) / SQLite (Local)
* **ORM:** SQLAlchemy
* **ID Standard:** UUID v7 (via `uuid6` library)
* **Language:** Python 3.12

## 🧠 Natural Language Search Logic

The `/api/profiles/search` endpoint implements a rule-based interpretation engine:

| Keyword | Mapping / Logic |
| :--- | :--- |
| **"young"** | Filters for ages between **16 and 24** |
| **"above X"** | Sets `min_age` to X |
| **"under X"** | Sets `max_age` to X |
| **"males/females"** | Filters by gender column |
| **"from [Country]"** | Maps country names (e.g., Nigeria, Kenya) to ISO Alpha-2 codes |

## 📡 API Reference

### 1. Natural Language Search
**Endpoint:** `GET /api/profiles/search`  
**Query Param:** `q=[search string]`  
**Example:** `/api/profiles/search?q=young males from nigeria`

### 2. Advanced Filtering
**Endpoint:** `GET /api/profiles`  
**Supported Params:** `gender`, `age_group`, `country_id`, `min_age`, `max_age`, `min_gender_probability`, `sort_by`, `order`, `page`, `limit`.  
**Example:** `/api/profiles?gender=female&min_age=21&sort_by=age&order=desc`

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <repo-folder>
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   The system will automatically seed the database on the first run.
   ```bash
   uvicorn main:app --reload
   ```

## ⚠️ Error Responses
All errors return a standardized JSON structure:
```json
{
  "status": "error",
  "message": "Invalid query parameters"
}
```

---
**Author:** [Your Name]  
**Task:** HNG Internship Stage 2 - Backend Track
```

Your documentation files are ready:
[file-tag: code-generated-file-1-1776924510324878700]