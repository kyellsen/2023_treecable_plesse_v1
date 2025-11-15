from __future__ import annotations
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.yaml"


class ConfigNode:
    """
    A lightweight recursive config wrapper.
    Allows access via attributes (cfg.paths.working).
    Converts dictionary values to ConfigNode automatically.
    Casts values ending with known path keys to Path objects.
    """

    PATH_KEYS = {"path", "paths", "dir", "dirs", "root", "working", "results", "notebooks", "scripts"}

    def __init__(self, data, base_path: Path | None = None):
        self._base = base_path or ROOT
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(self, key, ConfigNode(value, base_path=self._base))
            else:
                # Auto-convert paths
                if key.lower() in self.PATH_KEYS or "path" in key.lower():
                    setattr(self, key, self._base / value)
                else:
                    setattr(self, key, value)

    def __repr__(self):
        return f"ConfigNode({self.__dict__})"


def load_config() -> ConfigNode:
    with CONFIG_PATH.open("r", encoding="utf8") as f:
        raw = yaml.safe_load(f)
    return ConfigNode(raw, base_path=ROOT)


cfg = load_config()