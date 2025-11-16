from __future__ import annotations
from pathlib import Path
from typing import Any
import yaml

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.yaml"


class ConfigNode:
    """
    Rekursiver Wrapper:
    - Attributezugriff: cfg.paths.data
    - verschachtelte Dicts -> ConfigNode
    """

    def __init__(self, data: dict[str, Any]):
        for key, value in data.items():
            if isinstance(value, dict):
                value = ConfigNode(value)
            setattr(self, key, value)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def __repr__(self) -> str:
        return f"ConfigNode({self.__dict__})"


def _build_paths(raw_paths: dict[str, str], base: Path) -> ConfigNode:
    """
    Wandelt ALLE Werte unter 'paths' in absolute Path-Objekte um.
    - relative Pfade werden relativ zu 'base' interpretiert
    - absolute Pfade bleiben absolut
    """
    converted: dict[str, Path] = {}
    for key, value in raw_paths.items():
        p = Path(value)
        if not p.is_absolute():
            p = (base / p).resolve()
        else:
            p = p.resolve()
        converted[key] = p
    return ConfigNode(converted)


def load_config() -> ConfigNode:
    with CONFIG_PATH.open("r", encoding="utf8") as f:
        raw = yaml.safe_load(f)

    # Top-Level-Config aufbauen
    cfg_dict: dict[str, Any] = {}

    for key, value in raw.items():
        if key == "paths":
            cfg_dict["paths"] = _build_paths(value, ROOT)
        elif isinstance(value, dict):
            cfg_dict[key] = ConfigNode(value)
        else:
            cfg_dict[key] = value

    return ConfigNode(cfg_dict)


cfg = load_config()