import yaml
import os
import argparse

app_config = None
class Config:
    def __init__(self):
        parser = argparse.ArgumentParser(description="Example command-line argument parser")
        parser.add_argument('-c', '--config', type=str, help="Path to the configuration file")
        args = parser.parse_args()
        config_file = args.config
        print(config_file)
        self.config_file = config_file
        self.config_data = self._load_config()

    @staticmethod
    def load_config():
        global app_config
        try:
            app_config = Config()
            app_config._load_config()
        except Exception as e:
            print(f"Exception caught while loading config: {str(e)}")
            return False
        return True

    def _load_config(self):
        try:
            with open(self.config_file, 'r') as file:
                config_data = yaml.safe_load(file)
                return config_data
        except Exception as e:
            raise ValueError(f"Error loading config file: {e}")

    def get(self, key, default=None):
        # First, check if the key exists in the environment variables
        env_value = os.environ.get(key)
        if env_value:
            return env_value
        # If not found in environment variables, check if it exists in config data
        # If the key is not found in either config data or env, return the default value
        return self.config_data.get(key, default)

    def keys(self):
        return self.config_data.keys()

    def has_key(self, key):
        return key in self.config_data



