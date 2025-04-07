# app/core/config.py
import yaml
from pathlib import Path

class Config:
    def __init__(self, config_file="config/settings.yaml"):
        self.config = self.load_config(config_file)

    def load_config(self, config_file):
        with open(Path(config_file), "r") as file:
            return yaml.safe_load(file)

    def get(self, key, default=None):
        keys = key.split(".")
        value = self.config
        for k in keys:
            value = value.get(k, default)
            if value is None:
                return default
        return value

# Initialize a single config instance
config = Config()
