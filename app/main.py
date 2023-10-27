import config
import constants
from config import Config
from presidio_engine import PresidioEngine
from rule_sync import ObfuscateRuleSync
from server import Server

if __name__ == "__main__":
    if not Config.load_config():
        print("Failed to load config")
        exit(1)
    presidioEngine = PresidioEngine()

    redis_host = config.app_config.get(constants.REDIS_HOST, "localhost")
    redis_password = config.app_config.get(constants.REDIS_PASSWORD, "FuH0jXb9kt")
    redis_obfuscation_rules_db = config.app_config.get(constants.REDIS_OBFUSCATION_RULES_DB, 10)
    sync_interval = config.app_config.get(constants.REDIS_OBFUSCATION_RULES_SYNC_INTERVAL, 30)
    ruleSync = ObfuscateRuleSync(redis_host, 6379, redis_obfuscation_rules_db, redis_password, "zk_value_version",
                                 sync_interval, presidioEngine)
    ruleSync.sync_obfuscate_rules()

    port = config.app_config.get(constants.HTTP_PORT)
    server = Server(presidioEngine)
    server.app.run(host="0.0.0.0", port=port)
