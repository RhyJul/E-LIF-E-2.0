from __future__ import annotations

import sys
from pathlib import Path
from datetime import date, timedelta

# MUST be before importing from elife_app
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from elife_app.domain.models import DailyEntry
from sqlmodel import Session


class WellnessSeeder:
    """Seeds the database with sample wellness tracking data."""

    def seed(self, session: Session, days: int = 7) -> None:
        """
        Insert sample daily wellness entries for the past N days.

        Args:
            session: Database session
            days: Number of days of sample data to generate (default: 7)
        """
        entries = []
        today = date.today()

        for i in range(days):
            current_date = today - timedelta(days=i)
            entry = DailyEntry(
                date=current_date,
                sleep_quality=(i % 11),  # 0-10
                stress=(i % 11),  # 0-10
                friends=i % 2,  # 0-1
                water_intake=float((i % 6)),  # 0-5
                exercise=i % 2,  # 0-1
                mood=(i % 11),  # 0-10
                work_hours=float((i % 17)),  # 0-16
                hobbies=i % 2,  # 0-1
                steps=(i % 50001),  # 0-50000
                meds=i % 2,  # 0-1
                period=i % 2,  # 0-1
            )
            entries.append(entry)

        for entry in entries:
            session.add(entry)
        session.commit()

    def clear_all_entries(self, session: Session) -> None:
        """Clear all daily entries from the database."""
        session.query(DailyEntry).delete()
        session.commit()


if __name__ == "__main__":
    # For testing/development: seed the database with sample data
    from sqlmodel import create_engine, SQLModel

    engine = create_engine("sqlite:///elife.db", echo=False)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        seeder = WellnessSeeder()
        seeder.seed(session, days=30)
        print("✅ Database seeded with 30 days of sample wellness data")
