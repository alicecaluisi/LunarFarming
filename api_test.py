from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, date
from moonphase import moon_age_illum, phase_name
from gardening_tips import gardening_tips

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def waxing_or_waning(phase: str) -> str:
    return "waning" if "Waning" in phase or phase == "Full Moon" else "waxing"

def format_date_with_suffix(dt: date) -> str:
    day = dt.day
    suffix = "th" if 10 <= day % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    return f"{day}{suffix} {dt.strftime('%B %Y')}"

def build_report(dt: date) -> dict:
    age, illum_pct = moon_age_illum(dt)
    phase = phase_name(age)
    group = waxing_or_waning(phase)

    tips_month = gardening_tips.get(dt.month, {})
    tips = tips_month.get(group, "No gardening tips available.")
    maintenance = tips_month.get("maintenance", "")

    return {
        "date": format_date_with_suffix(dt),
        "age": round(age, 1),
        "illumination": round(illum_pct, 1),
        "phase": phase,
        "tips": tips,
        "maintenance": maintenance,
    }

@app.get("/")
def root():
    return {"status": "ok", "message": "Lunar Farming API is running"}

@app.get("/report")
def get_report(date_str: str = Query(..., description="Date in YYYY-MM-DD format")):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD."}

    return build_report(dt)

@app.get("/report/today")
def get_report_today():
    today = date.today()
    return build_report(today)
