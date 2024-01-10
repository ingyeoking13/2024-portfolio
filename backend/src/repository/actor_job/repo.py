from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session
from src.utils.yaml.yaml import load_settings
from src.dao.job.actor_job import ActorJob
from src.models.job.actor_job import ActorJob as actorJob
from src.utils.logger.logger import get_logger

_logger = get_logger(__file__)

class ActorJobRepo:
    def __init__(self) -> None:
        self.engine: Engine 
        self.engine = create_engine(
            **load_settings()['db']
        )
        ActorJob.metadata.create_all(self.engine)
    
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
    
    def add_job(self, job: actorJob):
        try: 
            with self.session as session:
                session.add(ActorJob(
                    name=job.name,
                    parent_name=job.parent_name,     
                    start_time=job.start_time, 
                    end_time=job.end_time,
                    result=job.result,
                    type=job.type
                    )
                )
        except Exception as e:
            _logger.exception(e)
            raise
        return True
    
    def set_result(self, job: actorJob) -> bool:
        with self.session as session:
            result = session.query(ActorJob).filter(
                ActorJob.name == job.name
            ).update({
                ActorJob.result: job.result,
                ActorJob.end_time: job.end_time
            })
        return True