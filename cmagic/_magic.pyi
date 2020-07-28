from typing import *


# noinspection PyShadowingBuiltins
class Magic:
    def __init__(
        self, debug: bool = False, symlink: bool = False,
        compress: bool = False,
        devices: bool = False,
        mime_type: bool = False,
        mime_encoding: bool = False,
        all: bool = False,
        check: bool = False,
        preserve_atime: bool = False,
        raw: bool = False,
        error: bool = False,
        no_check_apptype: bool = False,
        no_check_ascii: bool = False,
        no_check_compress: bool = False,
        no_check_elf: bool = False,
        no_check_fortran: bool = False,
        no_check_soft: bool = False,
        no_check_tar: bool = False,
        no_check_tokens: bool = False,
        no_check_troff: bool = False
    ):
        """
        Open libmagic database and create a Magic instance


        :param debug: Print debugging messages to stderr.
        :param symlink: If the file queried is a symlink, follow it.
        :param compress: If the file is compressed, unpack it and look at the contents.
        :param devices: If the file is a block or character special
                        device, then open the device and try to look in its contents.
        :param mime_type: Return a MIME type string, instead of a textual description.
        :param mime_encoding: Return a MIME encoding, instead of a textual description.
        :param all: Return all matches, not just the first.
        :param check: Check the magic database for consistency and print warnings to stderr.
        :param preserve_atime: On systems that support utime or utimes, attempt to
                               preserve the access time of files analyzed.
        :param raw: Don't translate unprintable characters to a \\ooo octal representation.
        :param error: Treat operating system errors while trying to open files and
                      follow symlinks as real errors, instead of printing them
                      in the magic buffer.
        :param no_check_apptype: Check for EMX application type (only on EMX).
        :param no_check_ascii: Check for various types of ascii files.
        :param no_check_compress: Don't look for, or inside compressed files.
        :param no_check_elf: Don't print elf details.
        :param no_check_fortran: Don't look for fortran sequences inside ascii files.
        :param no_check_soft: Don't consult magic files.
        :param no_check_tar: Don't examine tar files.
        :param no_check_tokens: Don't look for known tokens inside ascii files.
        :param no_check_troff: Don't look for troff sequences inside ascii files.
        """

    def set_flags(
            self, debug: bool = False, symlink: bool = False,
            compress: bool = False,
            devices: bool = False,
            mime_type: bool = False,
            mime_encoding: bool = False,
            all: bool = False,
            check: bool = False,
            preserve_atime: bool = False,
            raw: bool = False,
            error: bool = False,
            no_check_apptype: bool = False,
            no_check_ascii: bool = False,
            no_check_compress: bool = False,
            no_check_elf: bool = False,
            no_check_fortran: bool = False,
            no_check_soft: bool = False,
            no_check_tar: bool = False,
            no_check_tokens: bool = False,
            no_check_troff: bool = False
    ) -> None:
        """
        Open libmagic database and create a Magic instance


        :param debug: Print debugging messages to stderr.
        :param symlink: If the file queried is a symlink, follow it.
        :param compress: If the file is compressed, unpack it and look at the contents.
        :param devices: If the file is a block or character special
                        device, then open the device and try to look in its contents.
        :param mime_type: Return a MIME type string, instead of a textual description.
        :param mime_encoding: Return a MIME encoding, instead of a textual description.
        :param all: Return all matches, not just the first.
        :param check: Check the magic database for consistency and print warnings to stderr.
        :param preserve_atime: On systems that support utime or utimes, attempt to
                               preserve the access time of files analyzed.
        :param raw: Don't translate unprintable characters to a \\ooo octal representation.
        :param error: Treat operating system errors while trying to open files and
                      follow symlinks as real errors, instead of printing them
                      in the magic buffer.
        :param no_check_apptype: Check for EMX application type (only on EMX).
        :param no_check_ascii: Check for various types of ascii files.
        :param no_check_compress: Don't look for, or inside compressed files.
        :param no_check_elf: Don't print elf details.
        :param no_check_fortran: Don't look for fortran sequences inside ascii files.
        :param no_check_soft: Don't consult magic files.
        :param no_check_tar: Don't examine tar files.
        :param no_check_tokens: Don't look for known tokens inside ascii files.
        :param no_check_troff: Don't look for troff sequences inside ascii files.
        """

    def load(self, db_path: Optional[str] = None) -> None:
        """
        Must be used to load the the colon separated list
        of database files passed in as filename, or None for the
        default database file before any magic queries can performed.

        :param db_path: filename or None for the default database
                        The default database file is named by the MAGIC
                        environment variable. If that variable is not set,
                        the default database file name is /usr/share/misc/magic.
                        magic_load() adds ".mgc" to the database filename
                        as appropriate.
        """

    def check(self, db_path: Optional[str] = None) -> bool:
        """
        Can be used to check the validity of entries in the
        colon separated database files passed in as filename, or None
        for the default database. It returns True on success and False on failure.

        :param db_path: filename or None for the default database
                        The default database file is named by the MAGIC
                        environment variable. If that variable is not set,
                        the default database file name is /usr/share/misc/magic.
                        magic_load() adds ".mgc" to the database filename
                        as appropriate.
        """

    def compile(self, db_path: Optional[str]) -> bool:
        """
        Can be used to compile the the colon separated list of database
        files passed in as filename, or None for the default database.
        It returns True on success and False on failure.
        The compiled files created are named from the basename of each file
        argument with ".mgc" appended to it.

        :param db_path: filename or None for the default database
                        The default database file is named by the MAGIC
                        environment variable. If that variable is not set,
                        the default database file name is "/usr/share/misc/magic".
                        magic_load() adds ".mgc" to the database filename
                        as appropriate.
        """

    def guess_file(self, filename: str) -> str:
        """
        Returns a textual description of the contents of the filename argument.
        """

    def guess_bytes(self, payload: bytes) -> str:
        """
        Returns a textual description of the contents of the bytes argument
        """
