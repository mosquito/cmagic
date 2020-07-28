from cmagic import Magic, MAGIC_DB


def test_magic():
    m = Magic()

    assert m
    assert m.check(MAGIC_DB)

    m.load(MAGIC_DB)

    assert "ASCII text" in m.guess_file("/etc/hosts")
