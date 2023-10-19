import json
import threading

from app.models.obfuscate_rule import ObfuscateRule
from redis_client import RedisClient


class ObfuscateRuleSync:
    def __init__(self, redis_host, redis_port, redis_db, redis_password, hashset_name, interval_seconds=10):
        self.redis_client = RedisClient(host=redis_host, port=redis_port, db=redis_db, password=redis_password)
        self.hashset_name = hashset_name
        self.interval_seconds = interval_seconds

    def get_obfuscate_rule(self, obfuscate_rule_id):
        serialized_rule = self.redis_client.get_value_for_key(obfuscate_rule_id)
        if serialized_rule:
            return ObfuscateRule(**json.loads(serialized_rule))
        return None

    def fetch_and_process_obfuscate_rules(self):
        if not self.redis_client.is_connected():
            return
        rule_ids = self.redis_client.get_all_keys_from_hashset(self.hashset_name)
        for rule_id in rule_ids:
            obfuscate_rule = self.get_obfuscate_rule(rule_id)
            if obfuscate_rule:
                print(f"Synced ObfuscateRule {rule_id}: {obfuscate_rule.__dict__}")

    def sync_obfuscate_rules(self):
        threading.Timer(self.interval_seconds, self.sync_obfuscate_rules).start()
        try:
            if not self.redis_client.is_connected():
                self.redis_client.connect()
            self.fetch_and_process_obfuscate_rules()
        except Exception as e:
            print(f"Failed to sync obfuscate rules: {e}")

