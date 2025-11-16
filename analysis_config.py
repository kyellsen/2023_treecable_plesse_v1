from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.yaml"


class ConfigNode:
    """Generischer rekursiver Wrapper mit Attribut- und Itemzugriff."""

    def __init__(self, data: dict[str, Any]):
        for key, value in data.items():
            setattr(self, key, value)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def __repr__(self) -> str:
        return f"ConfigNode({self.__dict__})"


class PathsNode(ConfigNode):
    """Spezialknoten für Pfadstrukturen mit Hilfsfunktionen."""

    def ensure_all_dirs_exist(self) -> None:
        """
        Legt alle Path-Attribute rekursiv als Verzeichnisse an.
        """
        for key, value in self.__dict__.items():
            if key.startswith("_"):
                continue
            if isinstance(value, Path):
                value.mkdir(parents=True, exist_ok=True)
            elif isinstance(value, PathsNode):
                value.ensure_all_dirs_exist()
            elif isinstance(value, ConfigNode):
                # Falls man später weitere geschachtelte Nodes einführt
                for subkey, subval in value.__dict__.items():
                    if isinstance(subval, Path):
                        subval.mkdir(parents=True, exist_ok=True)


def _build_paths(raw: dict[str, Any], base: Path) -> PathsNode:
    """
    Baut rekursiv eine Pfadstruktur:
    - 'root' (falls vorhanden) definiert den Basisordner.
    - Alle weiteren Strings werden relativ zu diesem Basisordner interpretiert.
    - Verschachtelte Dicts werden erneut als PathsNode aufgebaut.
    """
    # Basis für diesen Block bestimmen
    root_rel = raw.get("root", "")
    if root_rel:
        root_path = (base / root_rel).resolve()
    else:
        root_path = base.resolve()

    converted: dict[str, Any] = {}

    for key, value in raw.items():
        if key == "root":
            converted["root"] = root_path
        elif isinstance(value, dict):
            # Verschachtelte Pfade nutzen den aktuellen root_path als Basis
            converted[key] = _build_paths(value, root_path)
        else:
            p = Path(value)
            if not p.is_absolute():
                p = (root_path / p).resolve()
            else:
                p = p.resolve()
            converted[key] = p

    return PathsNode(converted)


def load_config() -> ConfigNode:
    with CONFIG_PATH.open("r", encoding="utf8") as f:
        raw = yaml.safe_load(f)

    cfg_dict: dict[str, Any] = {}

    for key, value in raw.items():
        if key == "paths":
            paths_raw: dict[str, Any] = value
            paths_converted: dict[str, Any] = {}

            for pkey, pvalue in paths_raw.items():
                if isinstance(pvalue, dict):
                    # z.B. data, results → PathsNode mit root + Subpfaden
                    paths_converted[pkey] = _build_paths(pvalue, ROOT)
                else:
                    # einfache Pfade wie working, notebooks, scripts
                    p = Path(pvalue)
                    if not p.is_absolute():
                        p = (ROOT / p).resolve()
                    else:
                        p = p.resolve()from __future__ import annotations
from pathlib import Path
from typing import Any
import yaml

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.yaml"


class ConfigNode:
    """Generischer rekursiver Wrapper mit Attribut- und Itemzugriff."""

    def __init__(self, data: dict[str, Any]):
        for key, value in data.items():
            setattr(self, key, value)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def __repr__(self) -> str:
        return f"ConfigNode({self.__dict__})"


class PathsNode(ConfigNode):
    """Spezialknoten für Pfadstrukturen mit Hilfsfunktionen."""

    def ensure_all_dirs_exist(self) -> None:
        """
        Legt alle Path-Attribute rekursiv als Verzeichnisse an.
        """
        for key, value in self.__dict__.items():
            if key.startswith("_"):
                continue
            if isinstance(value, Path):
                value.mkdir(parents=True, exist_ok=True)
            elif isinstance(value, PathsNode):
                value.ensure_all_dirs_exist()
            elif isinstance(value, ConfigNode):
                # Falls man später weitere geschachtelte Nodes einführt
                for subkey, subval in value.__dict__.items():
                    if isinstance(subval, Path):
                        subval.mkdir(parents=True, exist_ok=True)


def _build_paths(raw: dict[str, Any], base: Path) -> PathsNode:
    """
    Baut rekursiv eine Pfadstruktur:
    - 'root' (falls vorhanden) definiert den Basisordner.
    - Alle weiteren Strings werden relativ zu diesem Basisordner interpretiert.
    - Verschachtelte Dicts werden erneut als PathsNode aufgebaut.
    """
    # Basis für diesen Block bestimmen
    root_rel = raw.get("root", "")
    if root_rel:
        root_path = (base / root_rel).resolve()
    else:
        root_path = base.resolve()

    converted: dict[str, Any] = {}

    for key, value in raw.items():
        if key == "root":
            converted["root"] = root_path
        elif isinstance(value, dict):
            # Verschachtelte Pfade nutzen den aktuellen root_path als Basis
            converted[key] = _build_paths(value, root_path)
        else:
            p = Path(value)
            if not p.is_absolute():
                p = (root_path / p).resolve()
            else:
                p = p.resolve()
            converted[key] = p

    return PathsNode(converted)


def load_config() -> ConfigNode:
    with CONFIG_PATH.open("r", encoding="utf8") as f:
        raw = yaml.safe_load(f)

    cfg_dict: dict[str, Any] = {}

    for key, value in raw.items():
        if key == "paths":
            paths_raw: dict[str, Any] = value
            paths_converted: dic_

                    paths_converted[pkey] = p

            cfg_dict["paths"] = ConfigNode(paths_converted)
        elif isinstance(value, dict):
            cfg_dict[key] = ConfigNode(value)
        else:
            cfg_dict[key] = value

    return ConfigNode(cfg_dict)


cfg = load_config()