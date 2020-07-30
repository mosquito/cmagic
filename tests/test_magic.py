import asyncio
from multiprocessing.pool import ThreadPool
from pathlib import Path

import pytest

from cmagic import Magic, find_db


@pytest.fixture
def magic():
    m = Magic()
    m.check(find_db())
    m.load(find_db())
    return m


def test_magic_find(magic):
    assert "ASCII text" in magic.guess_file("/etc/hosts")
    assert "ASCII text" in magic.guess_bytes(b"Hello world")

    result = magic.guess_bytes(
        b'\xcf\xfa\xed\xfe\x07\x00\x00\x01\x03\x00\x00\x00\x02\x00\x00\x00'
        b'\x12\x00\x00\x000\x07\x00\x00\x85\x00 \x00\x00\x00\x00\x00\x19'
    )
    assert 'Mach-O 64-bit x86_64 executable' in result

    magic.set_flags(mime_type=True)

    assert "text/plain" in magic.guess_file("/etc/hosts")
    assert "text/plain" in magic.guess_bytes(b"Hello world")


def test_magic_find_thread_safe(magic):
    pool = ThreadPool(32)

    m = Magic()

    assert m
    assert magic.check(find_db())

    magic.load(find_db())

    data = b'\xcf\xfa\xed\xfe\x07\x00\x00\x01\x03\x00\x00\x00\x02\x00\x00\x00'
    b'\x12\x00\x00\x000\x07\x00\x00\x85\x00 \x00\x00\x00\x00\x00\x19'

    for result in pool.imap_unordered(magic.guess_bytes, [data] * 32):
        assert 'Mach-O 64-bit x86_64 executable' in result

    magic.set_flags(mime_type=True)

    for result in pool.imap_unordered(magic.guess_bytes, [data] * 32):
        assert 'application/x-mach-binary' in result


def test_asyncio():
    from threading import local

    magic_tls = local()

    def get_instance():
        nonlocal magic_tls

        if not hasattr(magic_tls, "instance"):
            m = Magic(mime_type=True)
            m.load(find_db())
            magic_tls.instance = m

        return magic_tls.instance

    async def guess_file(fname):
        loop = asyncio.get_event_loop()

        def run():
            m = get_instance()
            return m.guess_file(fname)

        return await loop.run_in_executor(None, run)

    async def guess_bytes(payload):
        loop = asyncio.get_event_loop()

        def run():
            m = get_instance()
            return m.guess_bytes(payload)

        return await loop.run_in_executor(None, run)

    async def run():
        assert 'application/octet-stream' == await guess_bytes(b"\0\0\0\0\0")
        assert 'text/plain' == await guess_bytes(b"hello")

        result = await asyncio.gather(
            *[guess_file("/etc/hosts") for _ in range(30)]
        )

        assert len(result) == 30
        assert result == ['text/plain'] * 30

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()


DATA_FILES = Path(__file__).parent.resolve() / "data"


def test_extensions(magic):
    magic.set_flags(mime_type=True)

    pdf = str(DATA_FILES / "libmagic.pdf")
    txt = str(DATA_FILES / "libmagic.txt")
    elf = str(DATA_FILES / "linux.bin")
    marcho = str(DATA_FILES / "macos.bin")

    assert magic.guess_file(pdf) == 'application/pdf'
    assert magic.guess_file(txt) == 'text/plain'
    assert magic.guess_file(elf) == 'application/x-pie-executable'
    assert magic.guess_file(marcho) == 'application/x-mach-binary'

