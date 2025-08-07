from datetime import date, datetime
import math

LUNAR_MONTH = 29.530588861
EPOCH       = 2451550.09765          # 2000-01-06 18:14 TD

def true_phase(dt=None):
    if dt is None:
        dt = date.today()
    y, m = dt.year, dt.month
    k = math.floor((y + (m - 1)/12 - 2000) * 12.3685)   # lunations since 2000
    T = k / 1236.85
    T2, T3, T4 = T**2, T**3, T**4

    # mean phase in Julian Day (TD)
    jd = (EPOCH + LUNAR_MONTH * k
          + 0.0001337*T2 - 0.00000015*T3 + 0.00000000073*T4)
    return jd

def jd_from_date(d):
    y, m = d.year, d.month
    if m <= 2:
        y -= 1; m += 12
    A = y//100
    B = 2 - A + A//4
    return (math.floor(365.25*(y+4716)) +
            math.floor(30.6001*(m+1)) + d.day + B - 1524.5)

def moon_age_illum(dt=None):
    if dt is None:
        dt = date.today()
    jd_now = jd_from_date(dt)
    jd_last_new = true_phase(dt)         
    age = (jd_now - jd_last_new) % LUNAR_MONTH
    illum = (1 - math.cos(2*math.pi*age/LUNAR_MONTH))*50
    return age, illum

def phase_name(age):
    if   age <  1.84566:  return "New Moon"
    elif age <  5.53699:  return "Waxing Crescent"
    elif age <  9.22831:  return "First Quarter"
    elif age < 12.91963:  return "Waxing Gibbous"
    elif age < 16.61096:  return "Full Moon"
    elif age < 20.30228:  return "Waning Gibbous"
    elif age < 23.99361:  return "Last Quarter"
    elif age < 27.68493:  return "Waning Crescent"
    else:                 return "New Moon"