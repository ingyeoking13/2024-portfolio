from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from src.utils.yaml.yaml import load_settings
from src.dao.user.user import User

class UserRepo:
    def __init__(self) -> None:
        self.engine: Engine 
        engine = create_engine(
            **load_settings()['db']
        )
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        User.metadata.create_all(engine)
    
    @property
    def db(self) -> Session:
        db = self.session()
        return db
