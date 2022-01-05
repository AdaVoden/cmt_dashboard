import asyncio
import logging

from attr import define, field
from cmt_website.data.interfaces import DataReader, DataWriter


@define
class AsyncPoller:
    reader: DataReader = field()
    writer: DataWriter = field()

    async def run(self):
        while True:
            data = self.reader.read()
            self.writer.write(data)
