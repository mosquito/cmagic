import os

import pytest

from cmagic import Magic


@pytest.mark.skipif(not os.getenv("MAGIC"), reason="No any env db path")
def test_magic_env():
    m = Magic()

    assert m
    assert m.check()

    m.load()

    assert "ASCII text" in m.guess_file("/etc/hosts")
