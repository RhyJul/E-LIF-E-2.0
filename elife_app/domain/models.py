from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field

class DailyEntry(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  date: date
  sleep: int
  stress: int
  friends: int
  water: int
  exercise: int
  mood: int
  work_hours: float
  hobbies: int
  steps: int
  meds: int
  score: int = Field(default=0)
