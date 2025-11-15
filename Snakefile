###############################################
# Snakefile for 2023_treecable_plesse_v1
# Uses config.yaml in project root
###############################################

# -------------------------------
# Config einlesen (Root: config.yaml)
# -------------------------------
configfile: "config.yaml"

SCRIPTS   = config["paths"]["scripts"]
NOTEBOOKS = config["paths"]["notebooks"]
WORKING   = config["paths"]["working"]
RESULTS   = config["paths"]["results"]

threads: 4


# ---------------------------------------------
# Final target: all results needed for BA chapter
# ---------------------------------------------
rule all:
    input:
        # experiment-level overview (metadata etc.)
        f"{WORKING}/experiment_overview.parquet",
        # device-level features
        f"{WORKING}/ls3_features.parquet",
        f"{WORKING}/ptq_features.parquet",
        # f"{WORKING}/tms_features.parquet",  # TMS currently not used for Plesse
        # merged dataset
        f"{WORKING}/merged_events.parquet",
        # example analysis result table
        f"{RESULTS}/tables/plesse_A1_results.tex"


# ---------------------------------------------
# 100_experiment_overview.ipynb
# ---------------------------------------------
rule experiment_overview:
    output:
        f"{WORKING}/experiment_overview.parquet"
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


# ---------------------------------------------
# 200_merge_devices.ipynb – Merge LS3 + PTQ (+ context)
# ---------------------------------------------
rule merge_devices:
    input:
        overview = f"{WORKING}/experiment_overview.parquet",
        ls3      = f"{WORKING}/ls3_features.parquet",
        ptq      = f"{WORKING}/ptq_features.parquet"
        # tms   = f"{WORKING}/tms_features.parquet",  # optional später
    output:
        f"{WORKING}/merged_events.parquet"
    shell:
        r"""
        echo "Running 200_merge_devices (placeholder)"
        mkdir -p {WORKING}
        # später: uv run jupyter nbconvert --to notebook --execute \
        #   {NOTEBOOKS}/200_merge_devices.ipynb \
        #   --output {NOTEBOOKS}/200_merge_devices_exec.ipynb
        touch {output}
        """


# ---------------------------------------------
# 300_a1_example.ipynb – Example analysis A1
# ---------------------------------------------
rule analyse_A1:
    input:
        merged = f"{WORKING}/merged_events.parquet"
    output:
        f"{RESULTS}/tables/plesse_A1_results.tex"
    shell:
        r"""
        echo "Running 300_a1_example (placeholder)"
        mkdir -p {RESULTS}/tables
        # später: uv run jupyter nbconvert --to notebook --execute \
        #   {NOTEBOOKS}/300_a1_example.ipynb \
        #   --output {NOTEBOOKS}/300_a1_example_exec.ipynb
        echo "% Placeholder LaTeX content for A1 results" > {output}
        """
