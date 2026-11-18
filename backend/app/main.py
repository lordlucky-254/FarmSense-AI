from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .service import build_advice

app = FastAPI(title="FarmSense AI", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class FarmSnapshot(BaseModel):
    location: str = "Kenya"
    crop: str = "tomato"
    crop_symptoms: list[str] = Field(default_factory=list)
    poultry_symptoms: list[str] = Field(default_factory=list)
    rain_probability: float = Field(default=0.0, ge=0.0, le=1.0)
    temperature_c: float = Field(default=25.0, ge=-20, le=60)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "farmsense-api"}


@app.post("/api/v1/advice")
def advice(snapshot: FarmSnapshot) -> dict:
    return build_advice(snapshot.model_dump())
