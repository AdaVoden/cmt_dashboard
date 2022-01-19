import asyncio
from typing import Any, Coroutine, Tuple
import socket
import string
from asyncio.streams import StreamReader, StreamWriter
from typing import List
from hypothesis.strategies._internal.core import lists

import pytest
from cmt_website.data.sqm.pysqm_reader import (
    SQM,
    IPConnection,
    SQMConnector,
    SQMReader,
    _remove_non_digit_characters,
    make_sqm_reader,
)
from hypothesis import given
from hypothesis.strategies import text
from attr import field, define


async def echo(reader: StreamReader, writer: StreamWriter):
    data = await reader.read(100)
    writer.write(data)
    await writer.drain()
    writer.close()
    await writer.wait_closed()


@given(text(alphabet=string.printable))
def test_remove_characters(unclean):
    allowed = set(string.digits + ".")
    cleaned = set(_remove_non_digit_characters(unclean))
    assert cleaned.issubset(allowed)


class TestIPConnection:
    @pytest.mark.asyncio
    async def test_ip_connection(self, unused_tcp_port):
        server = await asyncio.start_server(
            echo, host="127.0.0.1", port=unused_tcp_port, family=socket.AF_INET
        )
        connection = IPConnection("127.0.0.1", unused_tcp_port)
        async with connection as conn, server as _:
            reader, writer = await conn
            writer.write("test".encode())
            await writer.drain()
            data = await reader.read(100)
            msg = data.decode()
            assert msg == "test"

    @pytest.mark.asyncio
    async def test_broken_connection(self):
        connection = IPConnection("127.0.0.1", 9999)
        with pytest.raises(ConnectionRefusedError):
            async with connection as conn:
                _, _ = await conn


@define
class DummyReader(StreamReader):
    list_of_strings: List[str] = field()

    async def read(self, n=-1):
        return ",".join(self.list_of_strings).encode()

    async def readline(self):
        pass

    async def readexactly(self, n):
        pass

    async def readuntil(self, separator=b"\n"):
        pass

    def at_eof(self):
        return True


@define
class DummyWriter(StreamWriter):
    def write(self, data):
        pass

    def writelines(self, data):
        pass

    def close(self):
        pass

    def can_write_eof(self):
        pass

    def write_eof(self):
        pass

    @property
    def transport(self):
        pass

    async def drain(self):
        pass

    def is_closing(self):
        pass

    async def wait_closed(self):
        pass


@define
class DummyConnection(SQMConnector):
    list_of_strings: List[str] = field()

    async def _dummy_stream(self):
        reader = DummyReader(self.list_of_strings)
        writer = DummyWriter()
        return reader, writer

    async def __aenter__(
        self,
    ) -> Coroutine[Any, Any, Tuple[StreamReader, StreamWriter]]:
        return self._dummy_stream()

    async def __aexit__(self, exception_type, exception_value, _) -> bool:
        if exception_type is None:
            return True
        else:
            return False


class TestSQMReader:
    @pytest.mark.asyncio
    @given(lists(text(min_size=1, max_size=15), min_size=1))
    async def test_dunder_read(self, list_of_strings):
        connection = DummyConnection(list_of_strings)
        reader = SQMReader(connection)
        first = list_of_strings[0]
        if first == "ix":
            rec = await reader._read(conn_type="metadata")
            assert rec == list_of_strings

        elif first == "cx":
            rec = await reader._read(conn_type="calibration")
            assert rec == list_of_strings

        elif first == "rx":
            rec = await reader._read(conn_type="data")
            assert rec == list_of_strings

        else:
            with pytest.raises(ValueError):
                await asyncio.wait_for(reader._read(conn_type=first), timeout=3)

    @pytest.mark.asyncio
    async def test_dunder_read_verified(self):
        connection = DummyConnection(["test"])
        reader = SQMReader(connection)
        with pytest.raises(RuntimeError):
            await asyncio.wait_for(reader._read(conn_type="metadata"), timeout=3)
