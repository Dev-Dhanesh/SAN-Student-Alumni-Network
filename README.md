# SAN – Student Alumni Network (Saveetha Alumni Network)

**Connect • Guide • Grow**  
*Your College Network. Your Career Advantage.*

---

## 🌟 Overview

**SAN** connects students, alumni, campus opportunities, and student project teams into a single college ecosystem.

### Core Capabilities
1. **Learn from Alumni**: Verified alumni directory with multi-filter search, multi-stage career journeys, interview experiences, and 1-on-1 mentorship requests.
2. **Discover Opportunities**: Central hub for internships, full-time jobs, hackathons, coding contests, and campus events.
3. **Team Matchmaker**: Intelligent 5-factor team matching engine pairing students based on complementary skills, shared interests, and event participation. Top matches glow green (`>= 70%`).
4. **Stories & Updates**: Community feed where alumni share office life, tech updates, and career advice, and students share hackathon recaps and project milestones.
5. **AI Career Roadmap**: Personalized milestone preparation pathways synthesized from alumni trajectories.

---

## 🛠️ Project Architecture

```
SAN-Saveetha Alumni Network/
├── frontend/
│   └── index.html                # High-performance SPA with constellation animation, dark theme, & API bridge
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI entrypoint, mounts API routers and serves frontend at /
│   │   ├── core/
│   │   │   ├── config.py         # Institutional settings, CORS, and keys
│   │   │   └── supabase.py       # Supabase service role client provider
│   │   ├── schemas/              # Pydantic v2 validation models
│   │   ├── services/
│   │   │   ├── matching_service.py # 5-factor deterministic team matching engine
│   │   │   ├── ai_service.py     # google-genai SDK + pattern synthesis fallback
│   │   │   ├── prep_analyzer.py  # Interview topic breakdown & frequency stats
│   │   │   ├── recommendation_service.py # Multi-entity recommendations
│   │   │   ├── journey_analyzer.py # Career trajectory extractor
│   │   │   └── demo_data.py      # Harmonized Saveetha demo dataset
│   │   └── api/
│   │       ├── alumni.py         # GET /api/alumni/
│   │       ├── opportunities.py  # GET & POST /api/opportunities/
│   │       ├── stories.py        # GET & POST /api/stories/
│   │       ├── matching.py       # POST /api/matching/find-teammates
│   │       ├── mentorship.py     # GET & POST /api/mentorship/
│   │       ├── roadmap.py        # POST /api/roadmap/generate
│   │       ├── analytics.py      # GET /api/analytics/interview-prep/{company}
│   │       ├── nl_search.py      # POST /api/search/nl
│   │       └── admin_compute.py  # Email verification & platform health stats
│   ├── tests/                    # 17 automated unit tests
│   ├── requirements.txt
│   └── run.py                    # Uvicorn launcher
└── supabase/
    ├── migrations/
    │   ├── 001_schema.sql        # Tables with pgvector & 1-to-1 profiles
    │   └── 002_rls.sql           # Row Level Security policies
    └── seed.sql                  # Ethical demo dataset
```

---

## 🚀 Quick Start Guide

### 1. Launch the Backend & Frontend Server
Navigate to the `backend/` directory and run:

```bash
cd backend
python run.py
```

### 2. Open the Application
Open your browser and navigate to:
👉 **`http://localhost:8000`**

- The complete **SAN** single-page web app will load immediately with the dark theme, hero animation, cards, and modals.
- Interactive Swagger API docs are available at **`http://localhost:8000/docs`**.

---

## 🧪 Running Automated Tests

Run the full automated test suite (17 tests covering matching, AI roadmap, interview analytics, and frontend integration):

```bash
python -m unittest discover -s backend/tests -p "test_*.py" -v
```

All 17 tests pass with 100% success.
