from __future__ import annotations
from sqlmodel import Session, select
from sqlalchemy.engine import Engine

import sys
from pathlib import Path
from datetime import date, timedelta
from typing import List, Optional

# Add workspace root to path for direct execution
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


# Handle both package imports and direct execution
try:
    from ..domain.models import DailyEntry
except ImportError:
    from elife_app.domain.models import DailyEntry


class BaseDAO:
    """Base class holding the SQLAlchemy/SQLModel engine."""

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def session(self) -> Session:
        """Create a new database session."""
        return Session(self.engine)


class DailyEntryDAO(BaseDAO):
    """DAO for wellness daily entry persistence and retrieval."""

    def create(self, entry: DailyEntry) -> DailyEntry:
        """Persist a DailyEntry and return the stored entry."""
        with self.session() as session:
            session.add(entry)
            session.commit()
            session.refresh(entry)
        return entry

    def get_by_date(self, entry_date: date) -> Optional[DailyEntry]:
        """Get a single daily entry by date."""
        with self.session() as session:
            statement = select(DailyEntry).where(DailyEntry.date == entry_date)
            return session.exec(statement).first()

    def get_by_id(self, entry_id: int) -> Optional[DailyEntry]:
        """Get a single daily entry by id."""
        with self.session() as session:
            return session.get(DailyEntry, entry_id)

    def list_all(self, limit: int = 100) -> List[DailyEntry]:
        """Return all entries newest-first, limited to recent entries."""
        with self.session() as session:
            statement = select(DailyEntry).order_by(
                DailyEntry.date.desc()).limit(limit)
            return list(session.exec(statement).all())

    def get_date_range(self, start_date: date, end_date: date) -> List[DailyEntry]:
        """Get entries within a date range (inclusive)."""
        with self.session() as session:
            statement = (
                select(DailyEntry)
                .where(DailyEntry.date >= start_date)
                .where(DailyEntry.date <= end_date)
                .order_by(DailyEntry.date.desc())
            )
            return list(session.exec(statement).all())

    def get_last_days(self, days: int = 7) -> List[DailyEntry]:
        """Get entries for the last N days."""
        end_date = date.today()
        start_date = end_date - timedelta(days=days - 1)
        return self.get_date_range(start_date, end_date)

    def update(self, entry: DailyEntry) -> DailyEntry:
        """Update an existing daily entry."""
        with self.session() as session:
            session.merge(entry)
            session.commit()
            return session.exec(select(DailyEntry).where(DailyEntry.id == entry.id)).first()

    def delete(self, entry_id: int) -> bool:
        """Delete a daily entry by id."""
        with self.session() as session:
            entry = session.get(DailyEntry, entry_id)
            if entry:
                session.delete(entry)
                session.commit()
                return True
            return False

    def get_average_score(self, days: int = 7) -> Optional[float]:
        """Get average wellness score for the last N days."""
        entries = self.get_last_days(days)
        if not entries:
            return None
        return sum(e.score for e in entries) / len(entries)


if __name__ == "__main__":
    # This allows the module to be imported and tested directly
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))

    from sqlmodel import create_engine

    print("✅ DailyEntryDAO module loaded successfully")
    print("Use: from elife_app.data_access.dao import DailyEntryDAO")
