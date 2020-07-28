import os

import pytest

from cmagic import Magic, MAGIC_DB


def test_magic():
    m = Magic()

    assert m
    assert m.check(MAGIC_DB)

    m.load(MAGIC_DB)

    assert "ASCII text" in m.guess_file("/etc/hosts")


@pytest.mark.skipif(not os.getenv("MAGIC"), reason="No any env db path")
def test_magic_env():
    m = Magic()

    assert m
    assert m.check()

    m.load()

    assert "ASCII text" in m.guess_file("/etc/hosts")
