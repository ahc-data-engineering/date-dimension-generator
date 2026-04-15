# Date Dimension Generator

Generates a fully populated date dimension table (`dim_dates`) in a SQL database, suitable for use in a data warehouse or BI environment.

## Features

Each date row includes:

### Gregorian calendar

- `key` — surrogate key in `YYYYMMDD` format (primary key)
- `isodate`, `year`, `month`, `day`
- `day_name`, `day_abbreviation`, `month_name`, `month_abbreviation`
- `day_of_week`, `day_of_year`, `week_of_month`
- `week`, `week_id`, `iso_week_date`
- `quarter`, `trimester`, `semester` — with `_id`, `first_day_of_`, `last_day_of_`, and `day_of_` variants
- `month_id`, `quarter_id`, `trimester_id`, `semester_id`
- `leap_year`, `is_weekend`, `is_first_day_of_month`, `is_last_day_of_month`
- `days_in_month`, `days_in_year`

### Business day

- `is_business_day` — `True` if the date is not a weekend and not a public holiday

### Fiscal calendar

- `fiscal_year`, `fiscal_quarter`, `fiscal_period` — fiscal period is the month number within the fiscal year (1–12)
- Configurable via `fiscal_year_start_month` (default: `1` for January)

### Holidays

- `is_holiday` — whether the date is a public holiday for the configured country
- `holiday` — name of the holiday, or `null`
- Powered by the [holidays](https://github.com/vacanza/python-holidays) library; supports many countries and languages

### Alternative calendars

Year, month, and day in each system:

- `islamic_*` — Hijri (Islamic) calendar
- `chinese_*` — Chinese lunar calendar (includes `chinese_is_leap_month`)
- `hebrew_*` — Hebrew calendar
- `persian_*` — Persian (Jalali/Solar Hijri) calendar
- `julian_day_number` — continuous Julian Day Number (noon-based, standard astronomical definition)

### ML / time-series features

- `cyclic_encoding` — `{"sine": float, "cosine": float}` encoding of the day's position within the year, suitable for use as features in machine learning models

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

```
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
print(d.julian_day_number)# 2460670
print(d.cyclic_encoding)  # {"sine": -0.103, "cosine": 0.995}
```

### Constructor parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
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
