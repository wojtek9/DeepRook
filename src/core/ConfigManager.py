import os
import json

from src.utils import utils


class ConfigManager:

    def __init__(self):
        self.config_path = self.get_config_path()
        self.config_data = self.load_config()

    @staticmethod
    def get_config_path():
        config_path = os.path.join(utils.get_temp_dir(), "DRConfig.json")

        # If file doesn't exist, create it with an empty JSON object
        if not os.path.exists(config_path):
            try:
                with open(config_path, "w") as f:
                    json.dump({}, f)
                print(f"Created new config file at {config_path}")
            except IOError as e:
                print(f"Failed to create config file: {e}")

        return config_path

    def load_config(self):
        if not os.path.exists(self.config_path):
            print("No existing config found. Using default settings.")
            return {}

        try:
            with open(self.config_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Failed to load config: {e}")
            return {}

    def save_config(self):
        try:
            with open(self.config_path, "w") as f:
                json.dump(self.config_data, f, indent=4)
            print(f"Config saved to {self.config_path}")
        except IOError as e:
            print(f"Failed to save config: {e}")

    def set(self, key, value):
        self.config_data[key] = value
        self.save_config()

    def get(self, key, default=None):
        return self.config_data.get(key, default)

    def set_config(self, config_dict):
        self.config_data = config_dict
        self.save_config()
