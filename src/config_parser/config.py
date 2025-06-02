import json
import os
import platform

from pathlib import Path


class Config:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = self.get_default_config_path()
        self.config_path = Path(config_path)
        self.config = self.load_config()

    def get_default_config_path(self) -> str:
        # Always use the config folder inside the project
        config_dir = Path(__file__).parent / "config"
        config_dir.mkdir(parents=True, exist_ok=True)  # Ensure the folder exists
        return str(config_dir / "config.json")

    def load_config(self) -> dict:
        if not self.config_path.exists():
            return {}
        with open(self.config_path, 'r') as file:
            return json.load(file)
