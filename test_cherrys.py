import unittest
import socket

try:
    import redis

    host, port = '127.0.0.1', 6379
    for res in socket.getaddrinfo(host, port, socket.AF_UNSPEC,
                                  socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        s = None
        try:
            s = socket.socket(af, socktype, proto)
            s.settimeout(1.0)
            s.connect((host, port))
            s.close()
        except socket.error:
            if s:
                s.close()
            raise
        break

except ImportError:

  class RedisSessionTest(unittest.TestCase):
      def test_nothing(self):
          self.fail("redis-py not available")

except socket.error:

  class RedisSessionTest(unittest.TestCase):
      def test_nothing(self):
          self.fail("redis not reachable")


else:

  class RedisSessionTest(unittest.TestCase):

      def test_something(self):
          self.assertTrue(True)

if __name__ == '__main__':
  unittest.main()
