from datetime import date, timedelta
import holidays

class DateDimension():
    d: date
    c: str

    def __init__(self, date: date = None, country: str = 'NL') -> None:
        self.d = date
        self.c = country

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
        return (date(self.d.year + 3 * self.quarter // 12, 3 * self.quarter % 12 + 1, 1) + timedelta(days=-1))
    
    @property
    def first_day_of_trimester(self) -> date:
        return date(self.d.year, 4 * (self.trimester - 1) + 1, 1)
    
    @property
    def last_day_of_trimester(self) -> date:
        return (date(self.d.year + 4 * self.trimester // 12, 4 * self.trimester % 12 + 1, 1) + timedelta(days=-1))
    
    @property
    def first_day_of_semester(self) -> date:
        return date(self.d.year, 6 * (self.semester - 1) + 1, 1)
    
    @property
    def last_day_of_semester(self) -> date:
        return (date(self.d.year + 6 * self.semester // 12, 6 * self.semester % 12 + 1, 1) + timedelta(days=-1))
    
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
        return self.d in holidays.country_holidays(country=self.c, years=self.d.year)
    
    @property
    def holiday(self) -> str:
        return holidays.country_holidays(country=self.c, years=self.d.year).get(self.d)
    
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
    def season(self) -> str:
        spring_start = date(self.year, 3, 20)
        summer_start = date(self.year, 6, 21)
        fall_start = date(self.year, 9, 22)
        winter_start = date(self.year, 12, 21)

        seasons = [
            { "is_season": spring_start <= self.isodate < summer_start, "season": "Spring" },
            { "is_season": summer_start <= self.isodate < fall_start, "season": "Summer" },
            { "is_season": fall_start <= self.isodate < winter_start, "season": "Autumn" },
            { "is_season": (self.isodate < spring_start) or (self.isodate >= winter_start), "season": "Winter" }
        ]

        return next((d.get("season") for d in seasons if d.get("is_season")))
    
    @property
    def week(self) -> int:
        return self.d.isocalendar().week
    
    @property
    def day_of_week(self) -> int:
        return self.d.isoweekday()

