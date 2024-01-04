from contextlib import contextmanager
from typing import Generator
import bcrypt

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session
from src.utils.yaml.yaml import load_settings
from src.dao.user.user import User
from src.models.user.auth import Auth
from src.utils.logger.logger import get_logger

_logger = get_logger(__file__)

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
    
    def add_user(self, auth: Auth):
        try: 
            salt = bcrypt.gensalt()
            with self.session as session:
                session.add(User(name=auth.name,
                    nickname=auth.nickname,     
                    email=auth.email, 
                    password=bcrypt.hashpw(
                        auth.password.encode('utf-8'),
                        salt
                    ),
                    salt=salt
                    ))
        except Exception as e:
            _logger.exception(e)
            raise
        return True
    
    def check_user_exist(self, name: str) -> bool:
        with self.session as session:
            result = session.query(User).filter(User.name == name).first()
        return result
    
    def check_password(self, auth: Auth) -> bool:
        with self.session as session:
            result = session.query(User).filter(User.name == auth.name).first()
            return bcrypt.checkpw(
                auth.password.encode('utf-8'),
                result.password.encode('utf-8')
            )
