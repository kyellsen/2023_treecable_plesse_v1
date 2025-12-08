###############################################
# Snakefile for 2023_treecable_plesse_v1
# Uses config.yaml in project root
###############################################

from pathlib import Path

configfile: "config.yaml"

SCRIPTS   = config["paths"]["scripts"]              # "scripts"
NOTEBOOKS = config["paths"]["notebooks"]            # "notebooks"
WORKING   = config["paths"]["working"]              # "working"

RESULTS_ROOT    = config["paths"]["results"]["root"]         # "../../400_results/..."
RESULTS_EXPORTS = f"{RESULTS_ROOT}/{config['paths']['results']['exports']}"
RESULTS_TABLES  = f"{RESULTS_ROOT}/{config['paths']['results']['tables']}"


threads: 1


# ---------------------------------------------
# Final target: all results needed for BA chapter
# ---------------------------------------------
rule all:
    input:
        # experiment-level overview (metadata etc.)
        f"{WORKING}/tree.parquet",
        f"{RESULTS_EXPORTS}/tree.csv",
        # device-level features
        # f"{WORKING}/ls3_features.parquet",
        # f"{WORKING}/ptq_features.parquet",
        # f"{WORKING}/tms_features.parquet",  # TMS currently not used for Plesse
        # merged dataset
        # f"{WORKING}/merged_events.parquet",
        # example analysis result table
        # f"{RESULTS_TABLES}/plesse_A1_results.tex"


# ---------------------------------------------
# 100_experiment_overview.ipynb
# ---------------------------------------------
rule experiment_overview:
    output:
        f"{WORKING}/tree.parquet",
        f"{RESULTS_EXPORTS}/tree.csv",
    shell:
        r"""
        echo "Running 100_experiment_overview (placeholder)"
        mkdir -p {WORKING}
        # später: uv run jupyter nbconvert --to notebook --execute \
        #   {NOTEBOOKS}/100_experiment_overview.ipynb \
        #   --output {NOTEBOOKS}/100_experiment_overview_exec.ipynb
        touch {output}
        """


# ---------------------------------------------
# 110_ls3.ipynb – LS3 pipeline
# ---------------------------------------------
rule ls3_pipeline:
    input:
        f"{WORKING}/experiment_overview.parquet"
    output:
        f"{WORKING}/ls3_features.parquet"
    shell:
        r"""
        echo "Running 110_ls3 (placeholder)"
        mkdir -p {WORKING}
        # später: uv run jupyter nbconvert --to notebook --execute \
        #   {NOTEBOOKS}/110_ls3.ipynb \
        #   --output {NOTEBOOKS}/110_ls3_exec.ipynb
        touch {output}
        """


# ---------------------------------------------
# 120_ptq.ipynb – PTQ pipeline
# ---------------------------------------------
rule ptq_pipeline:
    input:
        f"{WORKING}/experiment_overview.parquet"
    output:
        f"{WORKING}/ptq_features.parquet"
    shell:
        r"""
        echo "Running 120_ptq (placeholder)"
        mkdir -p {WORKING}
        # später: uv run jupyter nbconvert --to notebook --execute \
        #   {NOTEBOOKS}/120_ptq.ipynb \
        #   --output {NOTEBOOKS}/120_ptq_exec.ipynb
        touch {output}
        """


# ---------------------------------------------
# 130_tms.ipynb – (optional, aktuell deaktiviert)
# ---------------------------------------------
# rule tms_pipeline:
#     input:
#         f"{WORKING}/experiment_overview.parquet"
#     output:
#         f"{WORKING}/tms_features.parquet"
#     shell:
#         r"""
#         echo "Running 130_tms (placeholder)"
#         mkdir -p {WORKING}
#         # später: uv run jupyter nbconvert --to notebook --execute \
#         #   {NOTEBOOKS}/130_tms.ipynb \
#         #   --output {NOTEBOOKS}/130_tms_exec.ipynb
#         touch {output}
#         """
