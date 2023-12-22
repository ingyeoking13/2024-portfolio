from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from src.utils.yaml.yaml import load_settings

class UserRepo:
    def __init__(self) -> None:
        self.engine: Engine 
        engine = create_engine(
            **load_settings()['db'], 
            connect_args={"check_same_thread": False}
        )
        self.session: Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
