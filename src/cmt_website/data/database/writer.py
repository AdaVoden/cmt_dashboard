from attr import define, field
from cmt_website.data.interfaces import AsyncDataWriter
from sqlalchemy.engine import Engine


@define
class DBWriter(AsyncDataWriter):
    engine: Engine = field()

    async def write(self, data):
        pass
