import pandas as pd
from attr import define, field
from cmt_website.data.interfaces import DataReader
from sqlalchemy.engine.base import Engine


@define
class DBReader(DataReader):
    engine: Engine = field()
    table: str = field()

    def read(self) -> pd.DataFrame:
        pass
