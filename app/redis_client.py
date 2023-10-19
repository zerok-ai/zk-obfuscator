import redis


class RedisClient:
    def __init__(self, host: str, port=6379, db=0, password=None):
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db, password=password)

    def get_all_keys_from_hashset(self, hashset_name):
        return self.redis_client.hkeys(hashset_name)

    def get_value_for_key(self, key):
        # Retrieve the value for a specific key from Redis
        return self.redis_client.get(key)
