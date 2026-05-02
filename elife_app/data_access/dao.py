
from sqlmodel import Session, select
from data_access.db import engine
from domain.models import User, DailyEntry

# Registering users and login of users


class WellnessDAO:

    def register_user(self, user):
        with Session(engine) as session:
            session.add(user)
            session.commit()

    def login_user(self, username, password):
        with Session(engine) as session:
            statement = select(User).where(
                User.username == username,
                User.password == password
            )
            return session.exec(statement).first()

    def add_entry(self, entry):
        with Session(engine) as session:
            session.add(entry)
            session.commit()

    def get_user_entries(self, user_id):
        with Session(engine) as session:
            statement = select(DailyEntry).where(
                DailyEntry.user_id == user_id
            )
            return session.exec(statement).all()
