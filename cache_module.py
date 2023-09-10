import redis
from os import environ

REDIS_HOST = environ.get("REDIS_HOST")
REDIS_PORT = int(environ.get("REDIS_PORT"))
REDIS_PASSWORD = environ.get("REDIS_PASSWORD")

class Cache:
    def __init__(self):
        self.cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache.set(key, value)

    def delete(self, key):
        self.cache.delete(key)

    def flush(self):
        self.cache.flushdb()

    def get_all(self):
        return self.cache.keys('*')

    def get_all_values(self, keys):
        return self.cache.mget(keys)