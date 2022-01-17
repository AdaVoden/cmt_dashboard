import asyncio
import socket
import string
from asyncio.streams import StreamReader, StreamWriter

import pytest
from cmt_website.data.sqm.pysqm_reader import (SQM, IPConnection, SQMReader,
                                               _remove_non_digit_characters,
                                               make_sqm_reader)
from hypothesis import given
from hypothesis.strategies import text


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


@pytest.mark.asyncio
async def test_ip_connection(unused_tcp_port):
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
async def test_broken_connection():
    connection = IPConnection("127.0.0.1", 9999)
    with pytest.raises(ConnectionRefusedError):
        async with connection as conn:
            _, _ = await conn
