from __future__ import annotations

from typing import List, Optional

from sqlalchemy.engine import Engine
from sqlmodel import Session, select

from elife_app.domain.models import DailyEntry, User


class BaseDAO:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def session(self) -> Session:
        return Session(self.engine, expire_on_commit=False)


class EntryDAO(BaseDAO):

    def create(self, entry: DailyEntry) -> DailyEntry:
        with self.session() as session:
            session.add(entry)
            session.commit()
            session.refresh(entry)
            session.expunge(entry)
            return entry

    def list_all(self) -> List[DailyEntry]:
        with self.session() as session:
            results = session.exec(select(DailyEntry)).all()
            session.expunge_all()
            return list(results)

    def list_for_user(self, user_id: int) -> List[DailyEntry]:
        with self.session() as session:
            statement = (
                select(DailyEntry)
                .where(DailyEntry.user_id == user_id)
                .order_by(DailyEntry.date.desc())
            )
            results = session.exec(statement).all()
            session.expunge_all()
            return list(results)

    def get_by_id(self, entry_id: int) -> Optional[DailyEntry]:
        with self.session() as session:
            entry = session.get(DailyEntry, entry_id)
            if entry:
                session.expunge(entry)
            return entry


class UserDAO(BaseDAO):

    def create(self, user: User) -> User:
        with self.session() as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            session.expunge(user)
            return user

    def get_by_username(self, username: str) -> Optional[User]:
        with self.session() as session:
            user = session.exec(select(User).where(User.username == username)).first()
            if user:
                session.expunge(user)
            return user


class WellnessDAO:
    """Higher-level DAO used by the CLI app."""

    def __init__(self, engine: Engine | None = None) -> None:
        if engine is None:
            from elife_app.data_access.db import Database
            db = Database()
            self.engine = db.engine
        else:
            self.engine = engine

        self.user_dao = UserDAO(self.engine)
        self.entry_dao = EntryDAO(self.engine)

    def register_user(self, user: User) -> User:
        return self.user_dao.create(user)

    def login_user(self, username: str, password: str) -> Optional[User]:
        user = self.user_dao.get_by_username(username)
        if user and user.password == password:
            return user
        return None

    def add_entry(self, entry: DailyEntry) -> DailyEntry:
        return self.entry_dao.create(entry)

    def get_user_entries(self, user_id: int) -> List[DailyEntry]:
        return self.entry_dao.list_for_user(user_id)