from cmagic import Magic


def test_magic():
    m = Magic()

    assert m
    assert m.check()

    m.load()

    assert "ASCII text" in m.guess_file("/etc/hosts")
