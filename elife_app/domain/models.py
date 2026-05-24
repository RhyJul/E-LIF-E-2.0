from typing import List, Optional
from datetime import date, datetime
from zoneinfo import ZoneInfo
from sqlmodel import SQLModel, Field, Relationship

# Use Python 3.11.15 for sqlmodel otherwise an error will occur when
# running the app.


def swiss_time():
    """Return the current time in the Swiss timezone."""
    return datetime.now(ZoneInfo("Europe/Zurich"))


class User(SQLModel, table=True):
    """Represents a registered user of the wellness tracker."""

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str
    gender: str  # male / female

    daily_entries: List["DailyEntry"] = Relationship(back_populates="user")


class DailyEntry(SQLModel, table=True):
    """Represents one day's worth of wellness data for a user."""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=swiss_time)
    date: date
    sleep_quality: int = Field(ge=0, le=10)
    stress: int = Field(ge=0, le=10)
    friends: int = Field(ge=0, le=1)
    water_intake: float = Field(ge=0, le=5)
    exercise: int = Field(ge=0, le=1)
    mood: int = Field(ge=0, le=10)
    work_hours: float = Field(ge=0, le=16)
    hobbies: int = Field(ge=0, le=1)
    steps: int = Field(ge=0, le=50000)
    meds: int = Field(ge=0, le=1)
    period: int = Field(ge=0, le=1)
    period_pain: Optional[int] = Field(
        default=None, ge=0, le=10
    )  # Only relevant if period == 1
    period_flow: Optional[int] = Field(
        default=None, ge=0, le=3
    )  # Only relevant if period == 1
    score: int = Field(default=0)

    user: Optional[User] = Relationship(back_populates="daily_entries")

    class Config:
        validate_assignment = True


class Habit(SQLModel, table=True):
    """Represents a single habit observation linked to a daily entry."""

    id: Optional[int] = Field(default=None, primary_key=True)
    daily_entry_id: Optional[int] = Field(default=None, foreign_key="dailyentry.id")
    code: str  # e.g. "sleep", "stress", "water_intake"
    label: str  # human-readable name
    value_type: str  # "number" or "bool"
    value_number: Optional[float] = None
    value_bool: Optional[int] = None


class WellnessLog(SQLModel, table=True):
    """Stores the calculated wellness score for a daily entry."""

    id: Optional[int] = Field(default=None, primary_key=True)
    daily_entry_id: Optional[int] = Field(default=None, foreign_key="dailyentry.id")
    score: int
    algorithm_version: str = Field(default="1.0")
    calculated_at: datetime = Field(default_factory=swiss_time)


class Report(SQLModel, table=True):
    """Stores a generated wellness report for a daily entry."""

    id: Optional[int] = Field(default=None, primary_key=True)
    daily_entry_id: Optional[int] = Field(default=None, foreign_key="dailyentry.id")
    report_type: str  # "daily", "weekly", "monthly"
    created_at: datetime = Field(default_factory=swiss_time)
    content: str = Field(default="")
