from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Health Risk Scoring API",
    description="Demo FastAPI service for basic health risk scoring.",
    version="0.1.0",
)


class RiskInput(BaseModel):
    age: int
    smoker: bool
    bmi: float


class RiskOutput(BaseModel):
    risk_score: float
    risk_band: str


@app.get("/health", tags=["status"])
def health_check():
    return {"status": "ok"}


@app.post("/risk-score", response_model=RiskOutput, tags=["risk"])
def risk_score(payload: RiskInput):
    base = 0.0
    base += payload.age * 0.2
    if payload.smoker:
        base += 15
    base += max(payload.bmi - 25, 0) * 0.5

    if base < 20:
        band = "low"
    elif base < 40:
        band = "medium"
    else:
        band = "high"

    return RiskOutput(risk_score=round(base, 2), risk_band=band)
