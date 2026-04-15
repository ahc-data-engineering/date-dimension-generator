# Date Dimension Generator

Generates a fully populated date dimension table (`dim_dates`) in a SQL database, suitable for use in a data warehouse or BI environment.

## Fields

### Gregorian calendar

| Field | Type | Description |
| --- | --- | --- |
| `key` | `int` | Surrogate key in `YYYYMMDD` format — primary key |
| `isodate` | `date` | The date itself |
| `year` | `int` | Calendar year |
| `month` | `int` | Month number (1–12) |
| `day` | `int` | Day of the month (1–31) |
| `day_name` | `str` | Full weekday name (e.g. `Wednesday`) |
| `day_abbreviation` | `str` | Abbreviated weekday name (e.g. `Wed`) |
| `day_of_week` | `int` | ISO weekday number — Monday=1, Sunday=7 |
| `day_of_year` | `int` | Day number within the year (1–366) |
| `week_of_month` | `int` | Week number within the month (1–5), based on day number |
| `month_name` | `str` | Full month name (e.g. `December`) |
| `month_abbreviation` | `str` | Abbreviated month name (e.g. `Dec`) |
| `month_id` | `str` | Month identifier in `YYYYMmm` format (e.g. `2024M12`) |
| `week` | `int` | ISO week number (1–53) |
| `week_id` | `str` | ISO week identifier in `YYYYWww` format (e.g. `2024W52`) |
| `weeks_in_year` | `int` | Number of ISO weeks in the year — 52 or 53 |
| `iso_week_date` | `str` | Compact ISO 8601 week date in `YYYYww.d` format (e.g. `202452.3` for Wednesday of week 52, 2024) |
| `quarter` | `int` | Quarter number (1–4) |
| `quarter_id` | `str` | Quarter identifier in `YYYYQq` format (e.g. `2024Q4`) |
| `first_day_of_quarter` | `date` | First day of the quarter |
| `last_day_of_quarter` | `date` | Last day of the quarter |
| `day_of_quarter` | `int` | Day number within the quarter (1–92) |
| `trimester` | `int` | Trimester number (1–3); periods of four months: Jan–Apr, May–Aug, Sep–Dec |
| `trimester_id` | `str` | Trimester identifier in `YYYYTt` format (e.g. `2024T3`) |
| `first_day_of_trimester` | `date` | First day of the trimester |
| `last_day_of_trimester` | `date` | Last day of the trimester |
| `day_of_trimester` | `int` | Day number within the trimester (1–124) |
| `semester` | `int` | Semester number (1–2); Jan–Jun and Jul–Dec |
| `semester_id` | `str` | Semester identifier in `YYYYSs` format (e.g. `2024S2`) |
| `first_day_of_semester` | `date` | First day of the semester |
| `last_day_of_semester` | `date` | Last day of the semester |
| `day_of_semester` | `int` | Day number within the semester (1–184) |
| `leap_year` | `bool` | `True` if the year is a leap year |
| `days_in_month` | `int` | Number of days in the month (28–31) |
| `days_in_year` | `int` | Number of days in the year — 365 or 366 |
| `is_weekend` | `bool` | `True` if the date falls on a Saturday or Sunday |
| `is_first_day_of_month` | `bool` | `True` if the date is the first day of the month |
| `is_last_day_of_month` | `bool` | `True` if the date is the last day of the month |

### Business day

| Field | Type | Description |
| --- | --- | --- |
| `is_business_day` | `bool` | `True` if the date is not a weekend and not a public holiday |

### Fiscal calendar

Configurable via `fiscal_year_start_month` (default: `1` for January). The fiscal year is identified by the calendar year in which it starts.

| Field | Type | Description |
| --- | --- | --- |
| `fiscal_year` | `int` | Fiscal year — the calendar year in which the fiscal year starts |
| `fiscal_quarter` | `int` | Quarter within the fiscal year (1–4) |
| `fiscal_period` | `int` | Month number within the fiscal year (1–12) |

### Holidays

Powered by the [holidays](https://github.com/vacanza/python-holidays) library. Country and language are configured via the `country` and `language` constructor parameters.

| Field | Type | Description |
| --- | --- | --- |
| `is_holiday` | `bool` | `True` if the date is a public holiday in the configured country |
| `holiday` | `str\|null` | Name of the holiday, or `null` if not a holiday |

### Alternative calendars

| Field | Type | Description |
| --- | --- | --- |
| `islamic_year` | `int` | Year in the Hijri (Islamic) calendar |
| `islamic_month` | `int` | Month in the Hijri calendar (1–12) |
| `islamic_day` | `int` | Day in the Hijri calendar |
| `chinese_year` | `int` | Year in the Chinese lunar calendar |
| `chinese_month` | `int` | Month in the Chinese lunar calendar |
| `chinese_day` | `int` | Day in the Chinese lunar calendar |
| `chinese_is_leap_month` | `bool` | `True` if the date falls in an intercalary (leap) month |
| `hebrew_year` | `int` | Year in the Hebrew calendar |
| `hebrew_month` | `int` | Month in the Hebrew calendar |
| `hebrew_day` | `int` | Day in the Hebrew calendar |
| `persian_year` | `int` | Year in the Persian (Jalali/Solar Hijri) calendar |
| `persian_month` | `int` | Month in the Persian calendar |
| `persian_day` | `int` | Day in the Persian calendar |
| `julian_day_number` | `int` | Continuous Julian Day Number — days since noon, 1 January 4713 BC |

### ML / time-series features

| Field | Type | Description |
| --- | --- | --- |
| `days_since_epoch` | `int` | Days elapsed since 1970-01-01 — useful as a linear trend component |
| `year_fraction` | `float` | Position within the year as a value between 0.0 and 1.0 |
| `cyclic_day_of_year` | `dict` | Sine/cosine encoding with period 365/366 — captures yearly seasonality |
| `cyclic_day_of_week` | `dict` | Sine/cosine encoding with period 7 — captures within-week patterns |
| `cyclic_month` | `dict` | Sine/cosine encoding with period 12 — captures monthly seasonality |
| `cyclic_week_of_year` | `dict` | Sine/cosine encoding with period 52 or 53 — captures weekly patterns at yearly granularity |

All cyclic fields return `{"sine": float, "cosine": float}`.

## Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv)

## Installation

```bash
git clone https://github.com/arjan-hulshoff/date-dimension-generator
cd date-dimension-generator
uv sync
```

## Usage

Run interactively:

```bash
uv run program.py
```

You will be prompted for:

1. A SQLAlchemy connection string — e.g. `sqlite:///date_dimension.db` or `postgresql://user:password@localhost/mydb`
2. Start date in `yyyy-mm-dd` format
3. End date in `yyyy-mm-dd` format

The end date is **exclusive** — a range of `2024-01-01` to `2025-01-01` generates all dates in 2024.

### Example

```text
Provide the SQLAlchemy connection string: sqlite:///date_dimension.db
Enter start date (yyyy-mm-dd): 2020-01-01
Enter end date (yyyy-mm-dd): 2030-01-01
Execution time: 12.345
```

## Using `DateDimension` directly

```python
from datetime import date
from date_dimension import DateDimension

d = DateDimension(date(2024, 12, 25), country="NL", language="en_US")

print(d.key)              # 20241225
print(d.quarter)          # 4
print(d.is_holiday)       # True
print(d.holiday)          # "Christmas Day"
print(d.islamic_year)     # 1446
print(d.hebrew_year)      # 5785
print(d.julian_day_number)    # 2460670
print(d.cyclic_day_of_year)   # {"sine": -0.103, "cosine": 0.995}
```

### Constructor parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `date` | `datetime.date` | — | The date to represent |
| `country` | `str` | `"NL"` | ISO 3166-1 alpha-2 country code for holiday lookup |
| `language` | `str` | `"en_US"` | Language for holiday names (must be supported by the country) |
| `fiscal_year_start_month` | `int` | `1` | First month of the fiscal year (1–12) |

## Running tests

```bash
uv run pytest
```

## Notes

- Holiday detection uses the capital city of the configured country and defaults to the Netherlands (`NL`). See the [holidays library documentation](https://python-holidays.readthedocs.io) for supported countries and languages.
- The Chinese lunar calendar `chinese_is_leap_month` flag indicates whether the date falls in an intercalary (leap) month.
- The Julian Day Number follows the standard astronomical definition: JDN 0 = noon, 1 January 4713 BC (proleptic Julian calendar).
- The `trimester` divides the year into three periods of four months (Jan–Apr, May–Aug, Sep–Dec). This differs from academic trimesters.
