from date_dimension import DateDimension
from datetime import date, timedelta, datetime
from sqlalchemy import create_engine, Integer, String, Boolean, Date, JSON
from sqlalchemy.orm import sessionmaker, mapped_column, declarative_base, Session
from sqlalchemy_utils.functions import database_exists, create_database
from timeit import timeit
from typing import Generator


Base = declarative_base()


class DateTable(Base):
    __tablename__ = "dim_dates"

    iso_week_date = mapped_column(String, nullable=False)
    day = mapped_column(Integer, nullable=False)
    day_abbreviation = mapped_column(String, nullable=False)
    day_name = mapped_column(String, nullable=False)
    day_of_quarter = mapped_column(Integer, nullable=False)
    day_of_semester = mapped_column(Integer, nullable=False)
    day_of_trimester = mapped_column(Integer, nullable=False)
    day_of_week = mapped_column(Integer, nullable=False)
    day_of_year = mapped_column(Integer, nullable=False)
    first_day_of_quarter = mapped_column(Date, nullable=False)
    first_day_of_semester = mapped_column(Date, nullable=False)
    first_day_of_trimester = mapped_column(Date, nullable=False)
    holiday = mapped_column(String, nullable=True)
    is_holiday = mapped_column(Boolean, nullable=False)
    is_weekend = mapped_column(Boolean, nullable=False)
    isodate = mapped_column(Date, nullable=False)
    key = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=False, nullable=False
    )
    last_day_of_quarter = mapped_column(Date, nullable=False)
    last_day_of_semester = mapped_column(Date, nullable=False)
    last_day_of_trimester = mapped_column(Date, nullable=False)
    leap_year = mapped_column(Boolean, nullable=False)
    month = mapped_column(Integer, nullable=False)
    month_abbreviation = mapped_column(String, nullable=False)
    month_id = mapped_column(String, nullable=False)
    month_name = mapped_column(String, nullable=False)
    quarter = mapped_column(Integer, nullable=False)
    quarter_id = mapped_column(String, nullable=False)
    semester = mapped_column(Integer, nullable=False)
    semester_id = mapped_column(String, nullable=False)
    trimester = mapped_column(Integer, nullable=False)
    trimester_id = mapped_column(String, nullable=False)
    week = mapped_column(Integer, nullable=False)
    week_id = mapped_column(String, nullable=False)
    year = mapped_column(Integer, nullable=False)
    is_business_day = mapped_column(Boolean, nullable=False)
    is_first_day_of_month = mapped_column(Boolean, nullable=False)
    is_last_day_of_month = mapped_column(Boolean, nullable=False)
    days_in_month = mapped_column(Integer, nullable=False)
    days_in_year = mapped_column(Integer, nullable=False)
    fiscal_year = mapped_column(Integer, nullable=False)
    fiscal_quarter = mapped_column(Integer, nullable=False)
    fiscal_period = mapped_column(Integer, nullable=False)
    week_of_month = mapped_column(Integer, nullable=False)
    islamic_year = mapped_column(Integer, nullable=False)
    islamic_month = mapped_column(Integer, nullable=False)
    islamic_day = mapped_column(Integer, nullable=False)
    chinese_year = mapped_column(Integer, nullable=False)
    chinese_month = mapped_column(Integer, nullable=False)
    chinese_day = mapped_column(Integer, nullable=False)
    chinese_is_leap_month = mapped_column(Boolean, nullable=False)
    hebrew_year = mapped_column(Integer, nullable=False)
    hebrew_month = mapped_column(Integer, nullable=False)
    hebrew_day = mapped_column(Integer, nullable=False)
    persian_year = mapped_column(Integer, nullable=False)
    persian_month = mapped_column(Integer, nullable=False)
    persian_day = mapped_column(Integer, nullable=False)
    julian_day_number = mapped_column(Integer, nullable=False)
    cyclic_encoding = mapped_column(JSON, nullable=False)


_DATE_PROPS = [k for k, v in vars(DateDimension).items() if isinstance(v, property)]


def get_db(database_url: str) -> Session:
    engine = create_engine(
        database_url, pool_size=20, max_overflow=0, pool_recycle=3600, pool_timeout=60
    )
    if not database_exists(engine.url):
        create_database(engine.url)

    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return session_local()


def store_date_dimension(db: Session, startdate: date, enddate: date) -> None:
    for d in daterange(startdate, enddate):
        db.add(d)
    db.commit()


def daterange(startdate: date, enddate: date) -> Generator[DateTable, None, None]:
    for n in range(int((enddate - startdate).days)):
        dd = DateDimension(date=(startdate + timedelta(n)), country="NL", language="en_US")
        yield DateTable(**{k: getattr(dd, k) for k in _DATE_PROPS})


def main(database_url: str, startdate: date, enddate: date):
    db = get_db(database_url)
    execution_time = timeit(
        lambda: store_date_dimension(db, startdate, enddate), number=1
    )
    print(f"Execution time: {execution_time}")


if __name__ == "__main__":
    database_url = input(
        "Provide the SQLAlchemy connection string (e.g.: sqlite:///date_dimension.db): "
    )
    startdate = datetime.strptime(
        input("Enter start date (yyyy-mm-dd): "), "%Y-%m-%d"
    ).date()
    enddate = datetime.strptime(
        input("Enter end date (yyyy-mm-dd): "), "%Y-%m-%d"
    ).date()
    main(database_url, startdate, enddate)
