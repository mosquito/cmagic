cmagic
======

.. image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
   :target: https://saythanks.io/to/me@mosquito.su

.. image:: https://github.com/mosquito/cmagic/workflows/tox/badge.svg
    :target: https://github.com/mosquito/cmagic/actions?query=workflow%3Atox
    :alt: Github Actions

.. image:: https://img.shields.io/pypi/v/cmagic.svg
    :target: https://pypi.python.org/pypi/cmagic/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/wheel/cmagic.svg
    :target: https://pypi.python.org/pypi/cmagic/

.. image:: https://img.shields.io/pypi/pyversions/cmagic.svg
    :target: https://pypi.python.org/pypi/cmagic/

.. image:: https://img.shields.io/pypi/l/cmagic.svg
    :target: https://pypi.python.org/pypi/cmagic/

Python wrapper for libmagic.

Usage
-----

.. code-block::

   # MacOS
   $ export MAGIC=/usr/local/Cellar/libmagic/5.39/share/misc/magic.mgc

   # Ubuntu
   $ export MAGIC=/usr/lib/file/magic.mgc

.. code-block:: python

   import cmagic

   # Database path from MAGIC environment variable
   m = cmagic.Magic()

   if m.check():
      print("Database is ok")

   m.load()

   m.guess_file("/etc/hosts")
   # 'ASCII text'
   m.guess_bytes("hello world")
   # 'ASCII text'

   # Setting flags
   m.set_flags(mime_type=True)


   m = cmagic.Magic(
      # Setting flags here
      mime_type=True
   )

   # Trying to find database on the standard paths
   m.load(cmagic.find_db())

   m.guess_file("/etc/hosts")
   # 'text/plain'

   m.guess_bytes("hello world")
   # 'text/plain'


asyncio example
+++++++++++++++

.. code-block:: python

   import asyncio
   import cmagic
   from threading import local


   magic_tls = local()


   def get_instance():
       global magic_tls

       if not hasattr(magic_tls, "instance"):
           m = cmagic.Magic(mime_type=True)
           m.load(cmagic.find_db())
           magic_tls.instance = m

       return magic_tls.instance


   async def guess_file(fname):
       loop = asyncio.get_event_loop()

       def run():
           m = get_instance()
           return m.guess_file(fname)

       return await loop.run_in_executor(None, run)


   async def guess_bytes(payload):
       loop = asyncio.get_event_loop()

       def run():
           m = get_instance()
           return m.guess_bytes(payload)

       return await loop.run_in_executor(None, run)


   if __name__ == "__main__":
       print(asyncio.run(guess_file("/etc/hosts")))
       # text/plain
       print(asyncio.run(guess_bytes(b"\0\0\0\0\0\0\0")))
       # application/octet-stream


Installation
------------

Ubuntu/Debian
+++++++++++++

.. code-block:: bash

   apt-get install -y libmagic1 libmagic-mgc   # when using manilinux wheel
   apt-get install -y libmagic-dev             # for building from sources
   python3 -m pip install cmagic


Centos
++++++

.. code-block:: bash

   yum install -y file-libs            # when using manilinux wheel
   yum install -y file-devel           # for building from sources
   python3 -m pip install cmagic


MacOS
+++++

.. code-block:: bash

   brew install libmagic
   export CFLAGS="-I$(brew --prefix libmagic)/include" LDFLAGS="-L$(brew --prefix libmagic)/lib"
   python3 -m pip install cmagic
