from datetime import date, timedelta
from functools import cached_property
import holidays
from hijridate.convert import Gregorian
from lunardate import LunarDate
from pyluach.dates import HebrewDate
from jdatetime import date as JalaliDate
from math import pi, sin, cos


class DateDimension:
    d: date
    c: str

    def __init__(self, date: date, country: str = "NL", language: str = "en_US") -> None:
        self.d = date
        self.c = country
        self.l = language

    @property
    def iso_week_date(self) -> str:
        year, week, day_of_week = self.d.isocalendar()
        return f"{year:04d}{week:02d}.{day_of_week}"

    @property
    def year(self) -> int:
        return self.d.year

    @property
    def month(self) -> int:
        return self.d.month

    @property
    def day(self) -> int:
        return self.d.day

    @property
    def quarter(self) -> int:
        return (self.d.month - 1) // 3 + 1

    @property
    def trimester(self) -> int:
        return (self.d.month - 1) // 4 + 1

    @property
    def semester(self) -> int:
        return (self.d.month - 1) // 6 + 1

    @property
    def day_of_year(self) -> int:
        return self.d.timetuple().tm_yday

    @property
    def first_day_of_quarter(self) -> date:
        return date(self.d.year, 3 * (self.quarter - 1) + 1, 1)

    @property
    def last_day_of_quarter(self) -> date:
        return date(
            self.d.year + 3 * self.quarter // 12, 3 * self.quarter % 12 + 1, 1
        ) + timedelta(days=-1)

    @property
    def first_day_of_trimester(self) -> date:
        return date(self.d.year, 4 * (self.trimester - 1) + 1, 1)

    @property
    def last_day_of_trimester(self) -> date:
        return date(
            self.d.year + 4 * self.trimester // 12, 4 * self.trimester % 12 + 1, 1
        ) + timedelta(days=-1)

    @property
    def first_day_of_semester(self) -> date:
        return date(self.d.year, 6 * (self.semester - 1) + 1, 1)

    @property
    def last_day_of_semester(self) -> date:
        return date(
            self.d.year + 6 * self.semester // 12, 6 * self.semester % 12 + 1, 1
        ) + timedelta(days=-1)

    @property
    def day_of_quarter(self) -> int:
        return (self.d - self.first_day_of_quarter).days + 1

    @property
    def day_of_trimester(self) -> int:
        return (self.d - self.first_day_of_trimester).days + 1

    @property
    def day_of_semester(self) -> int:
        return (self.d - self.first_day_of_semester).days + 1

    @property
    def is_weekend(self) -> bool:
        return self.d.weekday() in [5, 6]

    @property
    def is_holiday(self) -> bool:
        return self.d in holidays.country_holidays(country=self.c, years=self.d.year, language=self.l)

    @property
    def holiday(self) -> str | None:
        return holidays.country_holidays(country=self.c, years=self.d.year, language=self.l).get(self.d)

    @property
    def key(self) -> int:
        return self.d.year * 10000 + self.d.month * 100 + self.d.day

    @property
    def week_id(self) -> str:
        return f"{self.d.isocalendar().year}W{self.d.isocalendar().week:>02}"

    @property
    def month_id(self) -> str:
        return f"{self.d.year}M{self.d.month:>02}"

    @property
    def quarter_id(self) -> str:
        return f"{self.d.year}Q{self.quarter}"

    @property
    def trimester_id(self) -> str:
        return f"{self.d.year}T{self.trimester}"

    @property
    def semester_id(self) -> str:
        return f"{self.d.year}S{self.semester}"

    @property
    def day_name(self) -> str:
        return f"{self.d:%A}"

    @property
    def day_abbreviation(self) -> str:
        return f"{self.d:%a}"

    @property
    def month_name(self) -> str:
        return f"{self.d:%B}"

    @property
    def month_abbreviation(self) -> str:
        return f"{self.d:%b}"

    @property
    def isodate(self) -> date:
        return self.d

    @property
    def leap_year(self) -> bool:
        return (self.year % 4 == 0 and self.year % 100 != 0) or (self.year % 400 == 0)

    @property
    def week(self) -> int:
        return self.d.isocalendar().week

    @property
    def day_of_week(self) -> int:
        return self.d.isoweekday()

    @cached_property
    def _hijri(self):
        return Gregorian(self.d.year, self.d.month, self.d.day).to_hijri()

    @cached_property
    def _lunar(self):
        return LunarDate.fromSolarDate(self.d.year, self.d.month, self.d.day)

    @cached_property
    def _hebrew(self):
        return HebrewDate.from_pydate(self.d)

    @cached_property
    def _persian(self):
        return JalaliDate.fromgregorian(day=self.d.day, month=self.d.month, year=self.d.year)

    @property
    def islamic_year(self) -> int:
        return self._hijri.year

    @property
    def islamic_month(self) -> int:
        return self._hijri.month

    @property
    def islamic_day(self) -> int:
        return self._hijri.day

    @property
    def chinese_year(self) -> int:
        return self._lunar.year

    @property
    def chinese_month(self) -> int:
        return self._lunar.month

    @property
    def chinese_day(self) -> int:
        return self._lunar.day

    @property
    def chinese_is_leap_month(self) -> bool:
        return self._lunar.isLeapMonth

    @property
    def hebrew_year(self) -> int:
        return self._hebrew.year

    @property
    def hebrew_month(self) -> int:
        return self._hebrew.month

    @property
    def hebrew_day(self) -> int:
        return self._hebrew.day

    @property
    def persian_year(self) -> int:
        return self._persian.year

    @property
    def persian_month(self) -> int:
        return self._persian.month

    @property
    def persian_day(self) -> int:
        return self._persian.day

    @property
    def julian_day_number(self) -> int:
        a = (14 - self.d.month) // 12
        y = self.d.year + 4800 - a
        m = self.d.month + 12 * a - 3
        return self.d.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045

    @property
    def cyclic_encoding(self) -> dict[str, float]:
        nbr_of_days: int = 366 if self.leap_year else 365
        fx: float = 2 * pi * self.day_of_year / nbr_of_days
        return {"sine": sin(fx), "cosine": cos(fx)}
