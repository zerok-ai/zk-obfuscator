import json
import threading

from models.obfuscate_rule import ObfuscateRule, AnalyzerConfig, AnonymizerConfig, AnonymizerOperator
from redis_client import RedisClient
from presidio_engine import presidio_engine_obj


class ObfuscateRuleSync:
    def __init__(self, redis_host, redis_port, redis_db, redis_password, hashset_name, interval_seconds):
        self.redis_client = RedisClient(host=redis_host, port=redis_port, db=redis_db, password=redis_password)
        self.hashset_name = hashset_name
        self.interval_seconds = interval_seconds

    def get_obfuscate_rule(self, obfuscate_rule_id):
        serialized_rule = self.redis_client.get_value_for_key(obfuscate_rule_id)
        if serialized_rule:
            string_data = serialized_rule.decode('utf-8')
            data = json.loads(string_data)
            obfuscate_rule = ObfuscateRule(id=data["id"], name=data["name"], updatedAt=data["updated_at"],
                                           analyzer=AnalyzerConfig(atype=data["analyzer"]["type"], pattern=data["analyzer"]["pattern"]),
                                           anonymizer=AnonymizerConfig(operator=AnonymizerOperator(data["anonymizer"]["operator"]),
                                                                       params=data["anonymizer"]["params"]))
            return obfuscate_rule

        return None

    def fetch_and_process_obfuscate_rules(self):
        if not self.redis_client.is_connected():
            return
        rule_ids = self.redis_client.get_all_keys_from_hashset(self.hashset_name)
        new_rules = []
        for rule_id in rule_ids:
            obfuscate_rule = self.get_obfuscate_rule(rule_id)
            if obfuscate_rule:
                print(f"Synced ObfuscateRule {rule_id}: {obfuscate_rule.__dict__}")
                new_rules.append(obfuscate_rule)
                print("Added to list.")
        presidio_engine_obj.updateObfuscationRules(new_rules)

    def sync_obfuscate_rules(self):
        threading.Timer(self.interval_seconds, self.sync_obfuscate_rules).start()
        try:
            if not self.redis_client.is_connected():
                self.redis_client.connect()
            self.fetch_and_process_obfuscate_rules()
        except Exception as e:
            print(f"Failed to sync obfuscate rules: {e}")

