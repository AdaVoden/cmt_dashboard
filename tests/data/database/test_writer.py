from cmt_website.data.database.models import Base
from sqlalchemy.engine import Engine
from sqlalchemy.engine.create import create_engine


def temp_memory_db(future=False):
    engine = create_engine("sqlite:///:memory:", echo=True, future=future)
    Base.metadata.create_all(engine)
    return engine
