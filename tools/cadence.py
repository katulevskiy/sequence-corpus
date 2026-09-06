"""Deterministic proposal cadence with weekends and quiet periods."""
from datetime import date, timedelta
import hashlib
import random
from zoneinfo import ZoneInfo

ZONE = ZoneInfo('Europe/Zagreb')


def activity(day):
    rng = random.Random(hashlib.sha256(f'corpus-cadence:{day}'.encode()).digest())
    year_rng = random.Random(day.year)
    vacation = date(day.year, 7, 15) + timedelta(days=year_rng.randrange(30))
    quiet = ((day.month == 12 and day.day >= 24) or
             (day.month == 1 and day.day <= 3) or
             vacation <= day < vacation + timedelta(days=8))
    chance = [.87, .88, .88, .86, .81, .54, .42][day.weekday()]
    if quiet or rng.random() > chance:
        return {'count': 0}
    return {'count': rng.choices([1, 2, 3, 4], [.16, .38, .32, .14])[0]}
