# Lunar Farming 🌙🌱

Lunar Farming is a small project that turns today’s Moon data into simple gardening guidance, with the long-term goal of becoming a lightweight backend that can power a mobile app.

It currently provides:
- **Moon age (in days)**
- **Illumination of the Moon (%)**
- **Lunar phase name**
- **Monthly gardening tips** on what to sow or transplant based on the lunar phase (waxing or waning), plus gardening maintenance advice.

---

## Why this exists

I live in the countryside and started my garden from scratch. At the beginning, I knew basically nothing, so I learned step by step: soil, seasons, watering, mistakes… and eventually I realized how relevant Moon phases are when sowing and planning work in the garden.

At the same time, I’m a physicist, so I wanted something that could compute the lunar phase (not just read it from a website), and expose it in a clean way that a simple CLI (and later a mobile UI) can consume. Lunar Farming is my “daily-use” bridge between real life and a small piece of astronomy math.


---

## Code overview

### Backend (core logic)

- `main.py`
  - CLI entrypoint that prints a daily report (date, Moon age, illumination, phase name) and selects the right gardening tips for the current month and waxing/waning family.

- `moonphase.py`
  - Core lunar calculations:
    - converts a calendar date/time into a Julian Day
    - estimates Moon age in days (time since the last New Moon, modulo the synodic month)
    - computes an approximate illuminated fraction
    - maps Moon age into one of the 8 classic phase names
  If you want the full explanation (math, assumptions, accuracy notes), see: `docs/moon-phase-math.md`. 
  

- `gardening_tips.py`
  - A simple month-based content layer:
    - what to focus on in the garden based on the lunar phase (waning or waxing)
    - a small maintenance advice paragraph
    - seasonal proverbs
   
### API (FastAPI)

- `api.py`
  - Main FastAPI app that exposes the daily report as JSON (CORS enabled for dev).
  - Endpoint: `GET /report` (optional `for_date=YYYY-MM-DD`) → returns `date`, `age_days`, `illumination_pct`, `phase`, `waxing_or_waning`, `tips`, `maintenance`.

- `api_test.py`
  - Not a unit test, but a small sandbox API to quickly validate the output/format.
  - Endpoints: `GET /` (healthcheck), `GET /report?date_str=YYYY-MM-DD`, `GET /report/today`.

---

## Quick start

### Requirements
- Python 3.x
- No external dependencies (standard library only)

### Run
```bash
python main.py
