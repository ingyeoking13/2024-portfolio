from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session
from src.utils.yaml.yaml import load_settings
from src.dao.job.task_job import TaskJob
from src.dao.utils import to_pydantic
from src.models.job.task_job import TaskJob as taskJob
from src.utils.logger.logger import get_logger

_logger = get_logger(__file__)

class TaskJobRepo:
    def __init__(self) -> None:
        self.engine: Engine 
        self.engine = create_engine(
            **load_settings()['db']
        )
        TaskJob.metadata.create_all(self.engine)
    
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
    
    def add_job(self, job: taskJob):
        try: 
            with self.session as session:
                session.add(TaskJob(
                    name=job.name,
                    parent_name=job.parent_name,     
                    start_time=job.start_time, 
                    end_time=job.end_time,
                    result=job.result,
                    type=job.type,
                    domain=job.domain,
                    sub_domain=job.sub_domain
                    )
                )
        except Exception as e:
            _logger.exception(e)
            raise
        return True
    
    def set_result(self, job: taskJob) -> bool:
        with self.session as session:
            result = session.query(TaskJob).filter(
                TaskJob.name == job.name
            ).update({
                TaskJob.result: job.result,
                TaskJob.end_time: job.end_time
            })
        return True
    
    def get_job(self, domain, sub_domain):
        with self.session as session:
            results = session.query(TaskJob)

            if domain is not None:
                results = results.filter(TaskJob.domain == domain)
            if sub_domain is not None:
                results = results.filter(TaskJob.sub_domain == sub_domain)
            
            results = results.all()
            return [taskJob(**to_pydantic(item)) for item in results]