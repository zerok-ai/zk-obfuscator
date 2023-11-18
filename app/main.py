from app import config
from app import constants
from app import rule_sync
from app import server
import uvicorn

if __name__ == "__main__":
    if not config.Config.load_config():
        print("Failed to load config")
        exit(1)

    redis_host = config.app_config.get(constants.REDIS_HOST, "localhost")
    redis_password = config.app_config.get(constants.REDIS_PASSWORD, "kj1p9v5tkB")
    redis_obfuscation_rules_db = config.app_config.get(constants.REDIS_OBFUSCATION_RULES_DB, 10)
    sync_interval = config.app_config.get(constants.REDIS_OBFUSCATION_RULES_SYNC_INTERVAL, 30)
    ruleSync = rule_sync.ObfuscateRuleSync(redis_host, 6379, redis_obfuscation_rules_db, redis_password, "zk_value_version",
                                 sync_interval)
    ruleSync.sync_obfuscate_rules()

    port = config.app_config.get(constants.HTTP_PORT)
    uvicorn.run(server.app, host="0.0.0.0", port=port)
