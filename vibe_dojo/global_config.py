"""Global configuration for Vibe-Dojo (user-level)."""

import json
from pathlib import Path
from typing import Optional

CONFIG_PATH = Path.home() / ".vibe_dojo_config"


def load_global_config() -> dict:
    """Load configuration from user home directory."""
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except:
            return {}
    return {}


def save_global_config(config: dict) -> None:
    """Save configuration to user home directory."""
    CONFIG_PATH.write_text(json.dumps(config, indent=2), encoding="utf-8")


def get_last_vault_path() -> Optional[Path]:
    """Get the last used vault path."""
    config = load_global_config()
    path_str = config.get("last_vault_path")
    if path_str:
        return Path(path_str)
    return None


def set_last_vault_path(path: Path) -> None:
    """Set the last used vault path."""
    config = load_global_config()
    config["last_vault_path"] = str(path.resolve())
    save_global_config(config)
