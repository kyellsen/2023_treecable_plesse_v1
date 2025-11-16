from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

# Basisordner dieses Analyse-Projekts (Verzeichnis von analysis_config.py)
ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.yaml"


class ConfigNode:
    """Einfacher Wrapper: Attribute- und Item-Zugriff auf ein Dict."""

    def __init__(self, data: dict[str, Any]):
        for key, value in data.items():
            setattr(self, key, value)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def __repr__(self) -> str:
        return f"ConfigNode({self.__dict__})"


class ResultsPaths(ConfigNode):
    """
    Pfadstruktur für Ergebnisse.

    ensure_all_dirs_exist():
      - legt alle Unterverzeichnisse (plots, tables, …) an
      - lässt 'root' unverändert (kein mkdir direkt auf root)
      - ist nicht-destruktiv (exist_ok=True)
    """

    def ensure_all_dirs_exist(self) -> None:
        for key, value in self.__dict__.items():
            if key.startswith("_") or key == "root":
                continue
            if isinstance(value, Path):
                value.mkdir(parents=True, exist_ok=True)


def _build_path_block(
    raw: dict[str, Any],
    base: Path,
    node_cls: type[ConfigNode],
) -> ConfigNode:
    """
    Baut einen Pfad-Block mit optionalem 'root' und Unterpfaden.

    - 'root' (falls vorhanden) definiert den Basisordner für diesen Block.
    - Alle String-Werte werden relativ zu diesem root interpretiert.
    - Ergebnis sind absolute Path-Objekte.
    """
    root_rel = raw.get("root", "")
    root_path = (base / root_rel).resolve() if root_rel else base.resolve()

    converted: dict[str, Any] = {}

    for key, value in raw.items():
        if key == "root":
            converted["root"] = root_path
        elif isinstance(value, dict):
            # verschachtelte Strukturen würden hier erneut als ConfigNode aufgebaut
            converted[key] = _build_path_block(value, root_path, ConfigNode)
        else:
            p = Path(value)
            if not p.is_absolute():
                p = (root_path / p).resolve()
            else:
                p = p.resolve()
            converted[key] = p

    return node_cls(converted)


def load_config() -> ConfigNode:
    with CONFIG_PATH.open("r", encoding="utf8") as f:
        raw = yaml.safe_load(f)

    cfg_dict: dict[str, Any] = {}

    for key, value in raw.items():
        if key == "paths":
            paths_raw: dict[str, Any] = value
            paths_converted: dict[str, Any] = {}

            for pkey, pvalue in paths_raw.items():
                # data: nur als Pfad-Struktur auflösen, aber nichts anlegen
                if pkey == "data" and isinstance(pvalue, dict):
                    paths_converted["data"] = _build_path_block(pvalue, ROOT, ConfigNode)

                # results: Pfad-Struktur mit ensure_all_dirs_exist()
                elif pkey == "results" and isinstance(pvalue, dict):
                    paths_converted["results"] = _build_path_block(pvalue, ROOT, ResultsPaths)

                # einfache Pfade wie working, notebooks, scripts
                else:
                    if isinstance(pvalue, dict):
                        # falls später weitere Blocks dazukommen
                        paths_converted[pkey] = _build_path_block(pvalue, ROOT, ConfigNode)
                    else:
                        p = Path(pvalue)
                        if not p.is_absolute():
                            p = (ROOT / p).resolve()
                        else:
                            p = p.resolve()
                        paths_converted[pkey] = p

            cfg_dict["paths"] = ConfigNode(paths_converted)

        elif isinstance(value, dict):
            cfg_dict[key] = ConfigNode(value)
        else:
            cfg_dict[key] = value

    return ConfigNode(cfg_dict)


cfg = load_config()


def ensure_output_dirs(config: ConfigNode | None = None) -> None:
    """
    Setup-Helfer:
      - legt den working-Ordner an
      - legt alle Unterverzeichnisse in results an (plots, tables, …)
      - roots (data.root, results.root) werden nicht direkt angelegt,
        können aber als Elternverzeichnisse durch die Subdirs entstehen.

    Nicht-destruktiv:
      - existierende Ordner bleiben unverändert
      - Inhalte werden nicht gelöscht oder überschrieben
    """
    if config is None:
        config = cfg

    paths = config.paths

    # working-Verzeichnis anlegen (falls definiert)
    working = getattr(paths, "working", None)
    if isinstance(working, Path):
        working.mkdir(parents=True, exist_ok=True)

    # results-Unterverzeichnisse anlegen (ohne root direkt anzufassen)
    results = getattr(paths, "results", None)
    if isinstance(results, ResultsPaths):
        results.ensure_all_dirs_exist()