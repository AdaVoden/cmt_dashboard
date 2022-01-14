import asyncio
from asyncio.exceptions import TimeoutError

import pytest
from cmt_website.data.interfaces import AsyncDataReader, AsyncDataWriter
from cmt_website.data.poller import AsyncPoller


class DummyReader(AsyncDataReader):
    def __init__(self, read_val, error: bool):
        self.read_val = read_val
        self.error = error

    async def read(self):
        if self.error:
            raise ValueError("Reader error thrown")
        else:
            return self.read_val


class DummyWriter(AsyncDataWriter):
    def __init__(self, error: bool):
        self.error = error

    async def write(self, data):
        if self.error:
            raise ValueError("Writer error thrown")
        else:
            return data


def test_breaking_reader():
    reader = DummyReader(0, True)
    writer = DummyWriter(False)
    with pytest.raises(ValueError):
        asyncio.run(AsyncPoller(reader, writer, delay=0).run())


def test_breaking_writer():
    reader = DummyReader(0, False)
    writer = DummyWriter(True)
    with pytest.raises(ValueError):
        asyncio.run(AsyncPoller(reader, writer, delay=0).run())


def test_working_poller():
    reader = DummyReader(0, False)
    writer = DummyWriter(False)

    async def runner():
        await asyncio.wait_for(AsyncPoller(reader, writer, delay=0).run(), timeout=0.1)

    with pytest.raises(TimeoutError):
        asyncio.run(runner())
