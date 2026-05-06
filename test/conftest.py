import pytest
from sqlmodel import Session, SQLModel

from elife_app.domain.models import DailyEntry
from elife_app.data_access.db import Database


@pytest.fixture(scope="function")
def database():
    db = Database("sqlite:///:memory:")
    SQLModel.metadata.create_all(db.engine)
    yield db
    SQLModel.metadata.drop_all(db.engine)


@pytest.fixture(scope="function")
def db(database):
    with Session(database.engine) as session:
        yield session


@pytest.fixture
def seeded_db(db):
    daily_entries = [
        DailyEntry(
            date="2023-01-01",
            sleep_quality=8,
            stress=3,
            friends=1,
            water_intake=2.5,
            exercise=1,
            mood=8,
            work_hours=8.0,
            hobbies=1,
            steps=10000,
            meds=0,
            period=0,
        ),
        DailyEntry(
            date="2023-01-02",
            sleep_quality=7,
            stress=4,
            friends=0,
            water_intake=3.0,
            exercise=0,
            mood=7,
            work_hours=7.5,
            hobbies=0,
            steps=8000,
            meds=1,
            period=0,
        ),
    ]
    db.add_all(daily_entries)
    db.commit()
    for daily_entry in daily_entries:
        db.refresh(daily_entry)
    return db


@pytest.fixture
def sample_items():
    return [20.0, 15.0]
