from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .service import generate_advice

app = FastAPI(title="FarmSense AI", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class AdviceRequest(BaseModel):
    weather: dict[str, Any] = Field(default_factory=dict)
    crop: dict[str, Any] = Field(default_factory=dict)
    poultry: dict[str, Any] = Field(default_factory=dict)
    activity: dict[str, Any] = Field(default_factory=dict)


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "model": "FarmSense Explainable Advisory Engine",
        "version": "2.0.0",
    }


@app.post("/api/v1/advice")
def get_advice(request: AdviceRequest) -> dict[str, Any]:
    return generate_advice(request.model_dump())
