from __future__ import annotations

from typing import List, Optional

from sqlalchemy.engine import Engine
from sqlmodel import Session, select

from ..domain.models import DailyEntry


class BaseDAO:
    """Base class holding the engine."""

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def session(self) -> Session:
        return Session(self.engine)


class EntryDAO(BaseDAO):
    """DAO for saving and loading daily entries."""

    def create(self, entry: DailyEntry) -> DailyEntry:
        with self.session() as session:
            session.add(entry)
            session.commit()
            session.refresh(entry)
            return entry

    def list_all(self) -> List[DailyEntry]:
        with self.session() as session:
            return list(session.exec(select(DailyEntry)).all())

    def get_by_id(self, entry_id: int) -> Optional[DailyEntry]:
        with self.session() as session:
            return session.get(DailyEntry, entry_id)