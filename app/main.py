import os
from app.server import Server
from rule_sync import ObfuscateRuleSync
from presidio_engine import PresidioEngine

DEFAULT_PORT = "9103"

if __name__ == "__main__":
    presidioEngine = PresidioEngine()
    ruleSync = ObfuscateRuleSync("localhost", 6379, 10, "FuH0jXb9kt", "zk_value_version", 10, presidioEngine)
    ruleSync.sync_obfuscate_rules()
    
    port = int(os.environ.get("PORT", DEFAULT_PORT))
    server = Server(presidioEngine)
    server.app.run(host="0.0.0.0", port=port)
