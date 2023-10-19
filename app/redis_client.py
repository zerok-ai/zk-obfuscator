import redis


class RedisClient:
    def __init__(self, host: str, port=6379, db=0, password=None):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = redis.StrictRedis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
            )
            self.connection.ping()
            return True
        except redis.exceptions.ConnectionError as e:
            print(f"Error connecting to Redis: {e}")
            self.connection = None
            return False

    def is_connected(self):
        try:
            if self.connection is not None:
                self.connection.ping()
                return True
            return False
        except (redis.exceptions.ConnectionError, AttributeError):
            return False

    def get_all_keys_from_hashset(self, hashset_name):
        return self.connection.hkeys(hashset_name)

    def get_value_for_key(self, key):
        # Retrieve the value for a specific key from Redis
        return self.connection.get(key)
