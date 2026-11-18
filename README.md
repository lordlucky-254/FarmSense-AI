# FarmSense AI

A modular smart-farming assistant that combines crop observations, poultry observations, weather context, and a farm activity log into one decision-support API.

FarmSense is the integration project. It does not claim to be a universal agricultural expert: every advisory has a source label, confidence level, and escalation rule. The starter runs with deterministic local logic so the product shape can be tested before adding hosted models, sensors, or paid APIs.

## Run

```bash
cd backend
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Use `frontend/index.html` for the responsive dashboard. API: `GET /health`, `POST /api/v1/advice`.

## Architecture boundaries

- `app/service.py`: replaceable advisory engine
- `app/main.py`: stable HTTP contract
- `frontend/`: thin client with no domain logic
- Future adapters: weather provider, PostgreSQL, crop model, poultry triage model, Kiswahili translation, and offline sync

## Safety

Weather alerts are informational. Crop and animal-health actions must be verified against local extension guidance. Do not use this starter to determine pesticide, antibiotic, or dosage decisions.
