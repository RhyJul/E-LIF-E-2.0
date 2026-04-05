from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field


class DailyEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: date
    sleep: int = Field(ge=0, le=10)
    stress: int = Field(ge=0, le=10)
    friends: int = Field(ge=0, le=1)
    water: float = Field(ge=0, le=10)
    exercise: int = Field(ge=0, le=1)
    mood: int = Field(ge=0, le=10)
    work_hours: float = Field(ge=0, le=24)
    hobbies: int = Field(ge=0, le=1)
    steps: int = Field(ge=0, le=50000)
    meds: int = Field(ge=0, le=1)
    period: int = Field(ge=0, le=1)
    period_pain: Optional[int] = Field(default=None, ge=0, le=10)
    period_flow: Optional[str] = Field(default=None)
    score: int = Field(default=0)
