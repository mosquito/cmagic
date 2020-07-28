cmagic
======

.. image:: https://coveralls.io/repos/github/mosquito/cmagic/badge.svg?branch=master
    :target: https://coveralls.io/github/mosquito/cmagic
    :alt: Coveralls

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

   m = cmagic.Magic()

   if m.check(cmagic.MAGIC_DB):
      print("Database is ok")

   m.load()

   m.guess_file("/bin/sh")
   # 'ASCII text'



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
   python3 -m pip install cmagic
