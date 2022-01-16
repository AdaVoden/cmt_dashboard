from typing import Dict

import numpy as np
import pandas as pd
from attr import define, field
from cmt_website.data.database.models import Base
from cmt_website.data.interfaces import DataReader
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


@define
class DBReader(DataReader):
    engine: Engine = field()
    table: Base = field()
    _columns: Dict[str, np.float64] = field(init=False)

    def __attrs_post_init__(self):
        columns = {column.name: np.float64 for column in self.table.__table__.columns}
        columns.pop("time")
        self._columns = columns

    def read(self) -> pd.DataFrame:
        stmt = select(self.table)
        with Session(self.engine) as session:
            return pd.read_sql_query(
                sql=stmt,
                con=session.bind,
                index_col="time",
                parse_dates=["time"],
                coerce_float=True,
                dtype=self._columns,
            )
