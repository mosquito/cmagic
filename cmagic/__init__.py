from pathlib import Path

from .version import __author__, __version__        # NOQA
from ._magic import Magic                           # NOQA

MAGIC_DB = Path(__file__).dirname / "magic.mgc"
