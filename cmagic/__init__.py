from glob import glob
from itertools import chain

from .version import __author__, __version__
from ._magic import Magic


def find_db():
    candidates = list(
        chain(
            glob("/usr/share/misc/magic.*"),
            glob("/usr/lib/file/magic.*"),
            glob("/usr/local/Cellar/libmagic/*/share/misc/magic.mgc"),
        )
    )

    if not candidates:
        raise RuntimeError("Magic database was not found")

    return candidates[0]


__all__ = ("Magic", "__author__", "__version__", "find_db")
