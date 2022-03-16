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

To tell CherryPy_ which backend to use, we need to specify the **storage_type**
for the **sessions** **tool**. You may want to read more about CherryPy_
configuration_.

::

    tools.sessions.storage_type : 'redis'

But CherryPy_ doesn't know Redis_. Hence the first thing we need to do is add
the cherrys **RedisSession** class to **cherrypy.lib.sessions**.

::

    import cherrys
    cherrypy.lib.sessions.RedisSession = cherrys.RedisSession

It is that simple!

Config dictionary
=================

There are 4 optional parameters you can set:

+ **host** *[127.0.0.1]* (when is_sentinel this is host for sentinel service)
+ **port** *[6379]* (when is_sentinel this is port for sentinel service)
+ **ssl** *[False]* (for both sentinel and redis)
+ **tls_skip_verify** *[False]* (for both sentinel and redis)

+ **is_sentinel** *[False]*
+ **sentinel_pass** *[None]*
+ **sentinel_service** *[None]*

+ **db** *[0]*
+ **prefix** *['cherrys_']* (prepended to session if, useful when ACLs are enabled)
+ **user** *[None]* (for old version of authentication can be set to empty string)
+ **password** *[None]*



A full config dictionary to activate Redis_ backed sessions would look like
this.

::

    config = {
        'tools.sessions.on' : True,
        'tools.sessions.storage_type' : 'redis',

        'tools.sessions.host': REDIS_HOST,
        'tools.sessions.port': REDIS_PORT,

        'tools.sessions.db': REDIS_DB,
        'tools.sessions.prefix': REDIS_PREFIX,
        'tools.sessions.user': REDIS_USER,
        'tools.sessions.password': REDIS_PASS,
        }

A full config dictionary to activate RedisSentinelSSL_ backed sessions would look like
this.

::

    config = {
        'tools.sessions.on' : True,
        'tools.sessions.storage_type' : 'redis',

        'tools.sessions.host': REDIS_HOST,
        'tools.sessions.port': REDIS_PORT,
        'tools.sessions.ssl': True,
        'tools.sessions.tls_skip_verify': True,

        'tools.sessions.is_sentinel': True,
        'tools.sessions.sentinel_pass': REDIS_SENTINEL_PASS,
        'tools.sessions.sentinel_service': REDIS_SENTINEL_SERVICENAME,

        'tools.sessions.db': REDIS_DB,
        'tools.sessions.prefix': REDIS_PREFIX,
        'tools.sessions.user': REDIS_USER,
        'tools.sessions.password': REDIS_PASS,
        }

.. _CherryPy: http://www.cherrypy.org
.. _PostgreSQL: http://www.postgresql.org
.. _Memcached: http://memcached.org
.. _Redis: http://redis.io
.. _dotCloud: http://www.dotcloud.com
.. _pip: http://pip-installer.org
.. _virtualenv: http://www.virtualenv.org
.. _redis-py: https://github.com/andymccurdy/redis-py
.. _hiredis-py: https://github.com/pietern/hiredis-py
.. _configuration: http://docs.cherrypy.org/stable/concepts/config.html
.. _RedisSentinelSSL: https://redis.io/topics/sentinel
