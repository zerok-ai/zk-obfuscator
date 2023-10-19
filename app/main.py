import os
from app.server import Server
from rule_sync import ObfuscateRuleSync

DEFAULT_PORT = "9103"

if __name__ == "__main__":
    ruleSync = ObfuscateRuleSync("localhost", 6379, 10, "EOa06dPNNT", "zk_value_version")
    ruleSync.sync_obfuscate_rules()
    port = int(os.environ.get("PORT", DEFAULT_PORT))
    server = Server()
    server.app.run(host="0.0.0.0", port=port)
