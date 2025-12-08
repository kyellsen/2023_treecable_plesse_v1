#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo ">> Running analysis in: $SCRIPT_DIR"

# 1) Environment strikt mit pyproject.toml / uv.lock synchronisieren
#    - legt .venv automatisch an, falls nicht vorhanden
echo ">> Syncing environment (pyproject.toml / uv.lock) via uv"
uv sync --all-extras

# 2) Snakemake im Projekt-Environment ausführen
echo ">> Starting Snakemake..."
uv run snakemake -j4 --rerun-incomplete --printshellcmds "$@"

echo ">> Analysis pipeline finished successfully."
