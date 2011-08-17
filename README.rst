===============================================
Cherrys : a Redis backend for CherryPy sessions
===============================================

CherryPy_ kicks some serious arse in the 'I am just a HTTP framework' category!
As of version 3.2 it supports 4 types of storage for sessions by default:

+ Ram
+ File
+ PostgreSQL_
+ Memcached_

Redis_ is growing in popularity as an alternative to Memcached_ (and is
fully supported on dotCloud_!)

Installation
============

If you are not using pip_ yet. Install it and while you are at it consider
using virtualenv_ too.

::

    $ pip install cherrys

redis-py_ and CherryPy_ are required dependencies hence will be installed if
necessary.

We recommend installing hiredis-py_ (a faster parser) as well.

::

    $ pip install hiredis

Usage (and abusage)
===================



.. _CherryPy: http://www.cherrypy.org
.. _PostgreSQL: http://www.postgresql.org
.. _Memcached: http://memcached.org
.. _Redis: http://redis.io
.. _dotCloud: http://www.dotcloud.com
.. _pip: http://pip-installer.org
.. _virtualenv: http://www.virtualenv.org
.. _redis-py: https://github.com/andymccurdy/redis-py
.. _hiredis-py: https://github.com/pietern/hiredis-py
