# import yaml
# import os
#
#
# class Config:
#     def __init__(self, file_path):
#         self.file_path = file_path
#         self.secrets = None
#         self.config_data = self._load_config()
#
#
#     def _load_config(self):
#         try:
#             with open(self.file_path, 'r') as file:
#                 config_data = yaml.safe_load(file)
#                 config_data.update(self.secrets)
#                 config_data.update(self.cluster_info_data)
#                 return config_data
#         except Exception as e:
#             raise ValueError(f"Error loading config file: {e}")
#
#     def get(self, key, default=None):
#         # First, check if the key exists in the environment variables
#         env_value = os.environ.get(key)
#         if env_value:
#             return env_value
#         # If not found in environment variables, check if it exists in config data
#         # If the key is not found in either config data or env, return the default value
#         return self.config_data.get(key, default)
#
#     def keys(self):
#         return self.config_data.keys()
#
#     def has_key(self, key):
#         return key in self.config_data
#
#
# configuration = Config("config/config.yaml")