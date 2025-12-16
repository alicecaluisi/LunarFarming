from datetime import date
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from moonphase import moon_age_illum, phase_name
from gardening_tips import gardening_tips


app = FastAPI()

# CORS per permettere a Flutter web (Chrome) di chiamare l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # in dev va bene così, poi si restringe
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def waxing_or_waning(phase: str) -> str:
    return "waning" if "Waning" in phase or phase == "Full Moon" else "waxing"


class MoonReport(BaseModel):
    date: str
    age_days: float
    illumination_pct: float
    phase: str
    waxing_or_waning: str
    tips: str | None = None
    maintenance: str | None = None


@app.get("/report", response_model=MoonReport)
def get_report(for_date: date | None = None):
    if for_date is None:
        for_date = date.today()

    age, illum_pct = moon_age_illum(for_date)
    phase = phase_name(age)
    group = waxing_or_waning(phase)

    month_tips = gardening_tips.get(for_date.month, {})
    tips = month_tips.get(group)
    maintenance = month_tips.get("maintenance")

    return MoonReport(
        date=for_date.isoformat(),
        age_days=round(age, 1),
        illumination_pct=round(illum_pct, 1),
        phase=phase,
        waxing_or_waning=group,
        tips=tips,
        maintenance=maintenance,
    )
