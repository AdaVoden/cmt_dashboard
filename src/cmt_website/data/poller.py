import asyncio
from abc import ABC, abstractmethod
from time import sleep

from attr import define, field
from cmt_website.data.interfaces import (AsyncDataReader, AsyncDataWriter,
                                         DataReader, DataWriter)


class PollerInterface(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError


@define
class AsyncPoller(PollerInterface):
    reader: AsyncDataReader = field()
    writer: AsyncDataWriter = field()
    delay: float = field()

    async def run(self):
        """Asynchronously reads from reader and writes to writer forever, with a delay
        in between read/write sessions"""
        while True:
            data = await self.reader.read()
            asyncio.create_task(self.writer.write(data))

            await asyncio.sleep(self.delay)


@define
class Poller(PollerInterface):
    reader: DataReader = field()
    writer: DataWriter = field()
    delay: float = field()

    def run(self):
        """BLOCKING Reads from reader and writes to writer forever, with small delay in seconds"""
        while True:
            data = self.reader.read()
            self.writer.write(data)

            sleep(self.delay)
