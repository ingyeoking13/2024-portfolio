from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from src.utils.yaml.yaml import load_settings
from src.dao.user.user import User

class UserRepo:
    def __init__(self) -> None:
        self.engine: Engine 
        self.engine = create_engine(
            **load_settings()['db']
        )
        User.metadata.create_all(self.engine)
    
    @property
    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        session = Session(self.engine)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
