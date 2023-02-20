"""
Cherrys is a Redis backend for CherryPy sessions.

The redis server must support SETEX https://redis.io/commands/setex.

Relies on redis-py https://github.com/andymccurdy/redis-py.
"""

try:
    import cPickle as pickle
except ImportError:
    import pickle

import redis
from cherrypy.lib.sessions import Session

REDIS_PORT = 6379


class RedisSession(Session):
    # the default settings
    host = '127.0.0.1'
    port = REDIS_PORT
    db = 0
    user = None
    password = None
    url = None
    ssl = False
    is_sentinel = False
    tls_skip_verify = False
    prefix = ""
    lock_prefix = "lock_"
    lock_timeout = None   # None, or time in secs until session lock expires
    ssl_cert_req = None
    sentinel_pass = None
    sentinel_service = None

    def __init__(self, *args, **kwargs):
        self.lock = None
        super().__init__(*args, **kwargs)

    @classmethod
    def setup(cls, **kwargs):
        """Set up the storage system for redis-based sessions.

        Called once when the built-in tool calls sessions.init.
        """
        # overwritting default settings with the config dictionary values
        for k, v in kwargs.items():
            setattr(cls, k, v)

        assert cls.prefix != cls.lock_prefix, "'prefix' must not be equal to 'lock_'"

        if cls.is_sentinel:
            if not cls.tls_skip_verify:
                cls.ssl_cert_req = "required"

            sentinel = redis.Sentinel(
                [(cls.host, cls.port)],
                ssl=cls.ssl,
                ssl_cert_reqs=cls.ssl_cert_req,
                sentinel_kwargs={
                    "password": cls.sentinel_pass,
                    "ssl": cls.ssl,
                    "ssl_cert_reqs": cls.ssl_cert_req
                },
                username=cls.user,
                password=cls.password
            )
            cls.cache = sentinel.master_for(cls.sentinel_service)
        elif cls.url:
            cls.cache = redis.from_url(cls.url)
        else:
            cls.cache = redis.Redis(
                host=cls.host,
                port=cls.port,
                db=cls.db,
                ssl=cls.ssl,
                username=cls.user,
                password=cls.password
            )

    @property
    def locked(self):
        return self.lock and self.lock.locked()

    def _exists(self):
        return bool(self.cache.exists(self.prefix + self.id))

    def _load(self):
        assert self.locked, "Cannot load data from unlocked session"
        try:
            return pickle.loads(self.cache.get(self.prefix + self.id))
        except TypeError:
            # if id not defined pickle can't load None and raise TypeError
            return None

    def _save(self, expiration_time):
        assert self.locked, "Cannot save data into unlocked session"
        pickled_data = pickle.dumps((self._data, expiration_time), pickle.HIGHEST_PROTOCOL)
        result = self.cache.setex(self.prefix + self.id, self.timeout * 60, pickled_data)

        if not result:
            raise AssertionError("Session data for id %r not set." % self.prefix + self.id)

    def _delete(self):
        assert self.locked, "Cannot delete unlocked session"
        self.cache.delete(self.prefix + self.id)

    def acquire_lock(self):
        """Acquire an exclusive redis lock on the currently-loaded session data."""
        self.lock = self.cache.lock(self.lock_prefix + self.id, timeout=self.lock_timeout)
        self.lock.acquire()

    def release_lock(self):
        """Release the lock on the currently-loaded session data."""
        if self.locked:  # lock might have expired already
            self.lock.release()
        self.lock = None
