import os
from multiprocessing.pool import ThreadPool

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
