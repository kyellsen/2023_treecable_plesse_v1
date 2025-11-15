#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------
# 1. Move into directory of this script
# ---------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo ">> Running analysis in: $SCRIPT_DIR"

# ---------------------------------------------
# 2. Activate local uv virtual environment
# ---------------------------------------------
if [ ! -d ".venv" ]; then
    echo ">> No virtual environment found. Creating..."
    uv venv
fi

echo ">> Using uv environment"
source .venv/bin/activate

# Ensure dependencies are installed
echo ">> Syncing dependencies with uv"
uv sync --all-extras

# ---------------------------------------------
# 3. Run snakemake pipeline
# ---------------------------------------------
echo ">> Starting Snakemake..."
uv run snakemake -j4 --rerun-incomplete --printshellcmds "$@"

# ---------------------------------------------
# DONE
# ---------------------------------------------
echo ">> Analysis pipeline finished successfully."
