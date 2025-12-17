# Moon phase math: how `moonphase.py` works

This document explains the physics behind `moonphase.py`, and how each function maps physics concepts into code.

---

## Key concepts

### 1. The synodic month: the lunar phase cycle
The visible lunar phases repeat with the synodic month, which is defined as the average time between two New Moons.

In the code, `LUNAR_MONTH = 29.530588861` is the value of the mean synodic month length near the J2000 era, commonly used in moon phase approximations.

### 2. Julian Day: a continuous time coordinate
Astronomy calculations are easier when dates are expressed as a single continuous number. Thus, a convertion from calendar dates to Julian Days is performed in the code. The Julian Day (JD) is the standard date used in astronomy calculations, since it counts days as real numbers.

### 3. The epoc
To compute the Moon age, a reference “zero point” is defined in the code: `EPOCH = 2451550.09765` is the Julian Ephemeris Day used as a reference New Moon close to the year 2000 (specifically, 2000-01-06 18:14 TD). This is a common choice in Meeus-style phase algorithms.

### 4. Mean phase vs true (high precision) phase
The code computes a mean New Moon time using a polynomial in time. It does not apply the periodic corrections given by the Sun/Moon anomalies, the argument of latitude and the planetary terms, used for true phase times, but uses a fast approximation, stable, simple, and accurate enough for daily gardening guidance, but not for precise phase timing.

---

## Function-by-function explanation

### `jd_from_date(d)`
Purpose: convert a Gregorian calendar date (`YYYY-MM-DD`) into Julian Day (JD).

What the algorithm is doing:
- January and February are treated as months 13 and 14 of the previous year. This makes the formula uniform.
- The terms `A` and `B` apply the Gregorian calendar correction.
- The `-1524.5` sets the JD reference so that JD rolls over at noon (historical convention).

In code:

```py
if m <= 2:
    y -= 1; m += 12
A = y//100
B = 2 - A + A//4
JD = floor(365.25*(y+4716)) + floor(30.6001*(m+1)) + d.day + B - 1524.5
```

---

### `true_phase(dt=None)`
Purpose: estimate the mean Julian Day of a New Moon near the month of `dt`.

Despite the name, it’s a mean phase model (not the fully corrected “true” phase time).

Step 1 — compute the lunation index `k`:
A lunation index is simply “how many New Moons since the epoch”.

```py
k = floor((y + (m - 1)/12 - 2000) * 12.3685)
```

- `y + (m-1)/12` expresses the start of the month as a fractional year.
- `12.3685` is an approximate number of synodic months per year (`365.2422 / 29.53059 ≈ 12.3685`).
- Taking `floor()` chooses the most recent lunation index at/before that month.

Step 2 — convert lunation index into a time variable `T`:
```py
T = k / 1236.85
```

`1236.85` is the conventional scaling used in Meeus-style phase formulas to express time in Julian centuries from the epoch.

Step 3 — mean New Moon time (polynomial):
```py
jd = EPOCH + LUNAR_MONTH*k + 0.0001337*T^2 - 0.00000015*T^3 + 0.00000000073*T^4
```

Interpretation:
- `EPOCH + LUNAR_MONTH*k` steps forward by `k` average lunar months from the reference New Moon.
- The polynomial terms adjust for slow long-term changes in the mean motion.

Note that, by design, the code is missing the periodic correction terms (the “wiggles” caused by elliptical orbits and perturbations), which are needed for high precision, but not for the purpose of this project.

---

### `moon_age_illum(dt=None)`
Purpose: produce two outputs:
1) Moon age (days into the cycle, 0..29.53)
2) Illumination (%) as a smooth periodic approximation

Step 1 — JD for the requested date:
```py
jd_now = jd_from_date(dt)
```

Step 2 — JD of the last mean New Moon:
```py
jd_last_new = true_phase(dt)
```

Step 3 — Moon age (days since New Moon):
```py
age = (jd_now - jd_last_new) % LUNAR_MONTH
```

Note: the modulo in the above formula ensures `age` to be always inside one cycle (`0 ≤ age < LUNAR_MONTH`), even if `jd_last_new` is not the immediately previous New Moon in a strict sense.

Step 4 — Illumination model:
```py
illum = (1 - cos(2*pi*age/LUNAR_MONTH))*50
```

This is a cosine-based phase model:
- Define a cycle angle: `θ = 2π * age / LUNAR_MONTH`
- New Moon → `θ = 0` → `cos(0)=1` → `illum=0`
- Full Moon → `θ = π` → `cos(π)=-1` → `illum=100`

So this produces a clean `0..100` percentage curve.

In a full geometric treatment, illumination relates to the Sun–Moon phase angle as seen from Earth, but in the code an approximation is made such that phase angle is advancing uniformly through the synodic month.

---

### `phase_name(age)`
Purpose: convert a continuous Moon age into one of the classic 8 phase labels.

The code uses thresholds that split the synodic month into standard “phase windows”:
- New Moon
- Waxing Crescent
- First Quarter
- Waxing Gibbous
- Full Moon
- Waning Gibbous
- Last Quarter
- Waning Crescent

This produces stable labels that match what most lunar calendars show.

---

## Accuracy and limitations

This model is intentionally approximate:
- It uses a mean synodic month and a mean New Moon estimate (polynomial only).
- It ignores the periodic correction terms that shift phase times by hours.
- It uses `date` (no time of day), so results can jump by up to ~1 day around phase boundaries.
- The epoch is in TD / ephemeris time, while `date.today()` is civil calendar time; the difference is small for this use case, but it matters for precision work.

---

## Resources used

- Meeus, J. (1998/2000). *Astronomical Algorithms* (2nd ed.). Willmann-Bell.

-  Urban, S. E., & Seidelmann, P. K. (Eds.). (2013). *Explanatory Supplement to the Astronomical Almanac* (3rd ed.). University Science Books.  

- U.S. Naval Observatory & HM Nautical Almanac Office. (Annual). *The Astronomical Almanac*.  

- Duffett-Smith, P., & Zwart, J. (2011). *Practical Astronomy with your Calculator or Spreadsheet* (4th ed.). Cambridge University Press.  