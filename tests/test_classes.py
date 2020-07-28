from cmagic import Magic


def test_magic():
    m = Magic()

    assert m
    assert m.check()

    m.load()

    assert "executable" in m.guess_file("/bin/sh")
