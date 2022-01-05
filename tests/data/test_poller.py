import pytest
from cmt_website.data.interfaces import DataReader, DataWriter
from cmt_website.data.poller import AsyncPoller


class DummyReader(DataReader):
    def __init__(self, read_val, error: bool):
        self.read_val = read_val
        self.error = error

    def read(self):
        if self.error:
            raise ValueError("Reader error thrown")
        else:
            return self.read_val


class DummyWriter(DataWriter):
    def __init__(self, error: bool):
        self.error = error

    def write(self, data):
        if self.error:
            raise ValueError("Writer error thrown")
        else:
            return data


def test_breaking_reader():
    reader = DummyReader(0, True)
    writer = DummyWriter(False)
    with pytest.raises(ValueError):
        AsyncPoller(reader, writer).run()


def test_breaking_writer():
    reader = DummyReader(0, False)
    writer = DummyWriter(True)
    with pytest.raises(ValueError):
        AsyncPoller(reader, writer).run()


def test_working_poller():
    reader = DummyReader(0, False)
    writer = DummyWriter(False)
    AsyncPoller(reader, writer).run()
