from datetime import date
from moonphase import moon_age_illum, phase_name   # from moonphase.py
from gardening_tips import gardening_tips          # from gardening_tips.py

def waxing_or_waning(phase: str) -> str:
    return "waning" if "Waning" in phase or phase == "Full Moon" else "waxing"

def format_date_with_suffix(dt: date) -> str:
    day = dt.day
    if 10 <= day % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    return f"{day}{suffix} {dt.strftime('%B %Y')}"

def adjust_month_for_hemisphere(month: int, hemisphere: str) -> int:
    """Shift month by 6 if user is in southern hemisphere."""
    if hemisphere.lower().startswith("s"):  
        return (month + 6 - 1) % 12 + 1
    return month

def print_report(dt: date, hemisphere: str = "north") -> None:
    age, illum_pct = moon_age_illum(dt)
    phase = phase_name(age)
    group = waxing_or_waning(phase)

    # Adjust month if southern hemisphere
    adjusted_month = adjust_month_for_hemisphere(dt.month, hemisphere)

    month_tips = gardening_tips.get(adjusted_month, {})
    tips = month_tips.get(group)
    maintenance = month_tips.get("maintenance")

    print(f"📅 Today is        : {format_date_with_suffix(dt)}")
    print(f"🌍 Hemisphere      : {hemisphere.capitalize()}")
    print(f"🌙 Age of the Moon : {age:.1f} days")
    print(f"💡 Illumination    : {illum_pct:.1f}%")
    print(f"🌕 Phase           : {phase}")

    if tips:
        print("\n"+tips)
    else:
        print("No gardening tips available for this month and lunar phase.")

    if maintenance:
        print("\n🧹 Maintenance advice:")
        print(maintenance)

if __name__ == "__main__":
    hemi = input("Which hemisphere are you in? (north/south): ").strip().lower()
    print_report(date.today(), hemi)
