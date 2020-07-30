from os import getenv, path
from glob import glob
from itertools import chain


__cached_db_path = None


def find_db():
    global __cached_db_path
    if __cached_db_path:
        return __cached_db_path

    env_path = getenv("MAGIC")

    if env_path and path.exists(env_path):
        __cached_db_path = env_path
        return __cached_db_path

    candidates = list(
        chain(
            glob("/usr/share/misc/magic.*"),
            glob("/usr/lib/file/magic.*"),
            glob("/usr/local/Cellar/libmagic/*/share/misc/magic.mgc"),
        )
    )

    if not candidates:
        raise RuntimeError("Magic database was not found")

    __cached_db_path = candidates[0]
    return __cached_db_path
