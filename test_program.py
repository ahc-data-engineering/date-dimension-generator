from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from program import Base, DateTable, daterange, store_date_dimension


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()


class TestDaterange:
    def test_row_count(self):
        rows = list(daterange(date(2024, 1, 1), date(2024, 1, 8)))
        assert len(rows) == 7

    def test_empty_range(self):
        rows = list(daterange(date(2024, 1, 1), date(2024, 1, 1)))
        assert rows == []

    def test_returns_date_table_instances(self):
        rows = list(daterange(date(2024, 1, 1), date(2024, 1, 2)))
        assert isinstance(rows[0], DateTable)

    def test_key_matches_date(self):
        rows = list(daterange(date(2024, 3, 15), date(2024, 3, 16)))
        assert rows[0].key == 20240315

    def test_consecutive_dates(self):
        rows = list(daterange(date(2024, 1, 1), date(2024, 1, 4)))
        assert [r.key for r in rows] == [20240101, 20240102, 20240103]


class TestStoreDateDimension:
    def test_row_count(self, db):
        store_date_dimension(db, date(2024, 1, 1), date(2024, 1, 8))
        assert db.query(DateTable).count() == 7

    def test_queryable_by_key(self, db):
        store_date_dimension(db, date(2024, 3, 15), date(2024, 3, 16))
        row = db.query(DateTable).filter_by(key=20240315).first()
        assert row is not None
        assert row.year == 2024
        assert row.month == 3
        assert row.day == 15

    def test_holiday_stored(self, db):
        store_date_dimension(db, date(2024, 12, 25), date(2024, 12, 26))
        row = db.query(DateTable).filter_by(key=20241225).first()
        assert row.is_holiday is True
        assert row.holiday == "Christmas Day"

    def test_cyclic_encoding_stored(self, db):
        store_date_dimension(db, date(2024, 1, 1), date(2024, 1, 2))
        row = db.query(DateTable).filter_by(key=20240101).first()
        for field in ("cyclic_day_of_year", "cyclic_day_of_week", "cyclic_month", "cyclic_week_of_year"):
            enc = getattr(row, field)
            assert isinstance(enc, dict)
            assert "sine" in enc
            assert "cosine" in enc
