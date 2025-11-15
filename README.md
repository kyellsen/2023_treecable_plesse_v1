# 2023 TreeCable Stuttgart Analysis

Dieses Projekt enthält die vollständige, reproduzierbare Analyse des Laborversuchs *2023 Stuttgart* im Rahmen der Bachelorarbeit.

## Projektstruktur

```
project_root/
├── config.yaml             # zentrale Konfiguration (Pfade, Geräte, Projekt-/Experiment-Infos)
├── analysis_config.py      # Python-Wrapper, der config.yaml als cfg lädt
├── Snakefile               # Snakemake-Pipeline (Orchestrierung aller Schritte)
├── run_analysis.sh         # Einstiegspunkt; startet Umgebung + Pipeline
├── notebooks/              # alle interaktiven Analyse-Notebooks
├── scripts/                # Hilfsfunktionen und utilities (Python-Skripte)
├── working/                # Zwischenergebnisse (wird nicht versioniert)
├── pyproject.toml          # Python-Umgebung (uv), Dependencies, Tooling
├── .vscode/                # Editor-Konfiguration
└── README.md               # Projektdokumentation
```

## Verwendung

### 1. Umgebung vorbereiten
Das Projekt verwendet **uv** für Python-Umgebungen und Paketmanagement.  
Beim ersten Start:

```
./run_analysis.sh
```

Das Skript:
- aktiviert oder erstellt `.venv/`
- synchronisiert Dependencies aus `pyproject.toml`
- startet die Snakemake-Pipeline

### 2. Analyse ausführen
Die gesamte Analyse-Pipeline wird über Snakemake gesteuert:

```
./run_analysis.sh
```

Optionen von Snakemake können direkt angehängt werden, z. B.:

```
./run_analysis.sh --dry-run
./run_analysis.sh -j8 --forceall
```

### 3. Konfiguration
Alle experiment- und projektbezogenen Einstellungen liegen zentral in:

```
config.yaml
```

Diese Datei definiert:
- Projekt- und Experiment-IDs
- Pfade (working, results, notebooks, scripts)
- aktivierte Geräte (LS3, PTQ, TMS)
- allgemeine Metadaten zur Analyse

Python-Notebooks und Skripte greifen direkt darauf zu via:

```python
from analysis_config import cfg
```

### 4. Pipeline-Orchestrierung
Die Datei:

```
Snakefile
```

definiert die gesamte Datenverarbeitung:
- Import & Cleaning
- Feature Engineering
- Merging
- Ergebnisgenerierung

Sie liest automatisch **config.yaml** ein und produziert reproduzierbare Workflows.

### 5. Notebooks
Im Ordner:

```
notebooks/
```

liegen alle interaktiven Analysen (Import, Cleaning, Feature Engineering, Visualisierung).  
Sie können standalone ausgeführt werden, werden aber auch automatisiert via Snakemake ausgeführt.

### 6. Scripts & Utilities
Eigenständige Python-Module oder Helper-Funktionen liegen in:

```
scripts/
```

Sie können in Notebooks und Snakemake-Regeln importiert werden.

---

## Ziel

Die Struktur ermöglicht:

- reproduzierbare Analysen  
- klare Trennung von Parametern, Code, Daten und Ergebnissen  
- Nutzbarkeit für andere Personen ohne Systemkenntnisse  
- saubere Veröffentlichung oder Archivierung der Bachelorarbeit  

Dieses Projekt ist so gestaltet, dass ein einzelner Befehl (`./run_analysis.sh`) die gesamte Pipeline auf jedem System reproduzierbar ausführen kann.

