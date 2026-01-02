"""Configuration management for Vibe-Dojo."""

from pathlib import Path
from typing import Optional

import yaml


class Config:
    """Configuration loader."""

    def __init__(self, vault_path: Optional[Path] = None):
        self.vault_path = Path(vault_path) if vault_path else Path.cwd()
        self.config_file = self.vault_path / "config.yaml"
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Load config from YAML file or return defaults."""
        if self.config_file.exists():
            with open(self.config_file, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        return self._default_config()

    def _default_config(self) -> dict:
        """Return default configuration."""
        return {
            "vault_path": ".",
            "llm": {
                "provider": "gemini",
                "model": "gemini-2.5-flash",
                "temperature": 0.3,
            },
            "defaults": {
                "timebox_min": 10,
                "confidence_threshold": 0.6,
                "max_drills_per_day": 5,
            },
        }

    def save(self):
        """Save current config to file."""
        with open(self.config_file, "w", encoding="utf-8") as f:
            yaml.dump(self.config, f, default_flow_style=False)
