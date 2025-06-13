import json
import yaml
from pathlib import Path


"""
Configuration file handler for the network automation project.

This module provides the Config class, which loads and manages configuration
data from a JSON file located in the 'config' folder inside the
'config_parser' package directory. If no path is specified, the default
location is 'src/config_parser/config/config.json' relative to the project root.

Classes:
    Config: Handles loading and accessing configuration data from a JSON file.

Usage:
    from config_parser.config import Config
    config = Config()  # Loads from default path
    config = Config(config_path="custom/path/to/config.json")  # Loads from custom path
    print(config.get_config())  # Access the configuration dictionary
"""
class Config:
    _instance = None  # Singleton instance

    def __new__(cls, config_path: str = None):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, config_path: str = None):
        if self._initialized:
            return
        if config_path is None:
            config_path = self.get_default_config_path()
        self.config_path = Path(config_path)
        self.config = self.load_config()
        self._initialized = True

    def get_default_config_path(self) -> str:
        config_dir = Path(__file__).parent / "config"
        config_dir.mkdir(parents=True, exist_ok=True)  # Ensure the folder exists
        return str(config_dir / "config.json")

    def load_config(self) -> dict:
        if not self.config_path.exists():
            return {}
        ext = self.config_path.suffix.lower()
        with open(self.config_path, 'r') as file:
            if ext in ['.yaml', '.yml']:
                return yaml.safe_load(file) or {}
            elif ext == '.json':
                return json.load(file)
            else:
                raise ValueError(f"Unsupported config file extension: {ext}")

    def reload_config(self):
        """Reload the configuration from file."""
        self.config = self.load_config()

    def get_config(self) -> dict:
        return self.config
