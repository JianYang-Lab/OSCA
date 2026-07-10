#!/usr/bin/env python3
"""
MCP Server for OSCA (OmicS-data-based Complex trait Analysis) v1.22

This MCP server exposes ALL OSCA functionality to AI tools (Claude, Codex, opencode)
through the Model Context Protocol. Users can invoke any OSCA analysis via natural language.

============================================================================
SETUP
============================================================================

1. Install Python dependency:
   pip install mcp

2. Configure your AI tool:

   ---- Claude Desktop ----
   Edit ~/Library/Application Support/Claude/claude_desktop_config.json:
   {
     "mcpServers": {
       "osca": {
         "command": "python3",
          "args": ["<OSCA_DIR>/osca-mcp/mcp_server.py"]
        }
      }
    }

    ---- opencode ----
    Edit .opencode.json or ~/.config/opencode/opencode.json:
    {
      "mcpServers": {
        "osca": {
          "type": "local",
          "command": ["python3", "<OSCA_DIR>/osca-mcp/mcp_server.py"]
        }
      }
    }

    ---- Codex (OpenAI) ----
    Edit ~/.codex/config.json:
    {
      "mcpServers": {
        "osca": {
          "command": "python3",
          "args": ["<OSCA_DIR>/osca-mcp/mcp_server.py"]
       }
     }
   }

   NOTE: Replace <OSCA_DIR> with the real path to the OSCA directory
         (the folder containing the osca binary).
         The OSCA binary must be in the same directory as this script.

============================================================================
AVAILABLE MCP TOOLS
============================================================================

1. osca_help(topic)     - Get OSCA documentation (overview/commands/flags/examples/formats)
2. run_osca(args, ...)  - Run any OSCA command with arbitrary flags
3. list_files(path)     - List files in a directory
4. read_file(path)      - Read contents of a file
5. osca_info()          - Get OSCA binary status and version info

============================================================================
EXAMPLE USAGE (what the AI agent would do)
============================================================================

User: "Create an ORM from my methylation data in meth.eFile"
AI:  calls run_osca(["--efile", "meth", "--methylation", "--make-orm", "--out", "meth_orm"])

User: "Run a linear regression association analysis"
AI:  calls run_osca(["--efile", "data", "--linear", "--pheno", "pheno.txt", "--out", "result"])

User: "What commands does OSCA support?"
AI:  calls osca_help("commands") then summarizes for the user

============================================================================
"""

import os
import sys
import json
import subprocess
import platform
import time
from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP

# ============================================================================
# Configuration
# ============================================================================

SCRIPT_DIR = Path(__file__).parent.resolve()
OSCA_BIN = (SCRIPT_DIR / ".." / "osca").resolve()

mcp = FastMCP("osca")


# ============================================================================
# OSCA Documentation Data
# ============================================================================

OSCA_DOCS = {

"overview": """OSCA (OmicS-data-based Complex trait Analysis) v1.22

OSCA is a C++ software tool developed by Yang Lab, Westlake University, for analyzing
complex traits using multi-omics data (DNA methylation, gene expression) and performing
genetic analysis of molecular phenotypes.

KEY CAPABILITIES:
- EWAS (Epigenome-Wide Association Study) with mixed linear model (MLM)
- eQTL and sQTL analysis (expression/splicing quantitative trait loci)
- ORM (Omic Relationship Matrix) computation analogous to GRM
- REML (Restricted Maximum Likelihood) variance component estimation
- PCA and Refactor for dimensionality reduction and cell-type deconvolution
- vQTL (variance QTL) analysis with multiple methods (Bartlett, Levene, DRM, SVLM)
- BESD (Binary eQTL Summary Data) format for summary statistics
- Meta-analysis (traditional and MeCS) and SMR (Summary-based Mendelian Randomization)
- Simulation of molecular phenotypes under various genetic models

SUPPORTED DATA FORMATS:
- EFile (.epi/.eii/.eed)        - OSCA's native omics data format
- BOD (.oii/.opi/.bod)          - Binary Omics Data format (compact storage)
- BFile (.bed/.bim/.fam)        - PLINK genotype format
- BESD                          - Binary eQTL Summary Data format
- ORM/GRM (.orm.bin/.grm.bin)   - Relationship matrices (binary or gzipped)

TYPICAL WORKFLOW:
1. Convert raw data to EFile format:  --make-efile
2. Quality control:                    --maf, --call, --sd-min, --impute-mean
3. Compute ORM:                        --make-orm
4. Run association analysis:           --mlma, --linear, --logistic, --moa
5. Or run eQTL/sQTL analysis:          --eqtl, --sqtl, --mlm

The OSCA binary is located alongside this MCP server script.
""",

"commands": """
OSCA COMMAND CATEGORIES (dispatched by priority - first matching flag wins)

=== 1. DATA MANAGEMENT & FORMAT CONVERSION ===
  --make-efile          Create EFile from text profile data
  --make-tefile         Create transposed EFile (probe-major to individual-major)
  --make-bod            Create BOD (Binary Omics Data) file from EFile
  --make-bld            Create BLD file from EFile
  --befile-flist        Merge multiple BESD files into one
  --update-opi          Update probe info file (.opi) with new annotation

=== 2. RELATIONSHIP MATRIX COMPUTATION ===
  --make-orm            Compute ORM (Omic Relationship Matrix) in binary format
  --make-orm-gz         Compute ORM in gzipped format
  --orm-alg <n>         ORM algorithm: 1=standardize probes, 2=center probes, 3=standardize individuals

=== 3. QUALITY CONTROL & DATA EXPLORATION ===
  --get-variance        Calculate and output variance for each probe
  --get-mean            Calculate and output mean for each probe
  --impute-mean         Impute missing values with probe mean
  --pca [n]             Principal component analysis (output n PCs, default 20)
  --refactor <n>        Refactor analysis for cell-type deconvolution (n = number of PCs)
  --score               Calculate polygenic/score for individuals
  --blup-probe          BLUP (Best Linear Unbiased Prediction) for probes
  --probes-independent <n>  Extract a set of independent probes (n = target number)

=== 4. ASSOCIATION ANALYSIS ===
  --linear              Linear regression association analysis
  --logistic            Logistic regression association analysis
  --assoc               Basic association analysis (unadjusted)
  --mlma                Mixed linear model association (MLMA) - accounts for relatedness
  --mlma-loco           Leave-One-Chromosome-Out MLMA (function implemented but
                        not dispatched in option() - partially implemented feature)
  --moa                 MOA (Moment of Association) - efficient mixed-model method
  --moa-exact           Exact MOA (uses exact rather than approximate moment calculations)
  --moment              Moment-based analysis (alternative to MOA)
  --moment-exact        Exact moment analysis
  --moment2-beta        Moment2-beta analysis (second-order moment with beta approximation)
  --vqtl                Variance QTL analysis (identifies variants affecting variance)
                        Methods: Bartlett, Levene_mean, Levene_median, Fligner_Killeen,
                        drm (Deviation Regression Model), svlm (Squared Value Linear Model)
  --eqtl                eQTL analysis (expression quantitative trait loci)
  --mlm                 eQTL analysis with mixed linear model
  --sqtl                sQTL analysis (splicing quantitative trait loci)

=== 5. REML & VARIANCE COMPONENT ANALYSIS ===
  --reml                REML (Restricted Maximum Likelihood) variance component estimation
  --reml-pred-rand      Predict random effects (BLUP) in REML
  --reml-est-fix        Estimate fixed effects in REML

=== 6. META-ANALYSIS & SUMMARY STATISTICS ===
  --meta                Traditional inverse-variance weighted meta-analysis
  --mecs                MeCS (Meta-analysis of cis-eQTL Summary statistics) method
  --query [p]           Query BESD database for significant associations (default p=5e-8)
  --gc                  Genomic control for EWAS summary statistics
  --to-smr              Convert BESD to SMR (Summary-based Mendelian Randomization) format
  --make-besd           Create BESD file from eQTL summary statistics
  --make-besd-dense     Create dense BESD file
  --besd-shrink         Shrink BESD file (remove null associations)
  --diff                Compare two BESD files and report differences

=== 7. SIMULATION ===
  --simu-qt             Simulate quantitative molecular phenotypes
  --simu-cc             Simulate case-control molecular phenotypes
  --simu-reverse        Reverse causal simulation
""",

"flags": """
COMPLETE OSCA FLAG REFERENCE (v1.22)

All flags use the format: --flag-name [value]  (brackets indicate optional value)

============================================================================
INPUT / OUTPUT FILES
============================================================================
--efile <prefix>              EFile prefix for omics data (.epi/.eii/.eed will be appended)
--tefile <prefix>             Transposed EFile prefix (.tepi/.teii/.teed)
--bfile <prefix>              PLINK BFile prefix (.bed/.bim/.fam)
--befile <prefix>             BESD file prefix (for eQTL summary data)
--out <prefix>                Output file prefix (default: "osca")
--pheno <file>                Phenotype file (PLINK format: FID IID pheno)
--mpheno <col>                Phenotype column number (1-based, for multi-phenotype files)
--covar <file>                Categorical covariate file (PLINK format)
--qcovar <file>               Quantitative covariate file (PLINK format)
--covar-bod <file>            Covariate in BOD format
--covar-efile <prefix>        Covariate in EFile format
--covar-tefile <prefix>       Covariate in transposed EFile format
--bed <file>                  BED file (for sQTL analysis with leafcutter)
--keep <file>                 File listing individuals to keep in analysis
--remove <file>               File listing individuals to remove from analysis
--pheno-bod <file>            Phenotype in BOD format (used by DRM/SVLM vQTL module)
--geno <file>                 Genotype file prefix (used by DRM/SVLM vQTL module)
--freq-file <file>            Frequency file for allele frequency data
--var-file <file>             Variance file for probe variance data
--eff-file <file>             Effect file (for adding environmental effects)
--eff-probe <file>            Effect probe list file
--add-eff                     Add environmental effect (N(0,sd)) to each probe
--eff-n                       Use effective sample size
--score-has-header            Indicate that score file has a header row
--save-r2                     Save R-squared values during analysis
--r2-thresh <val>             R-squared threshold (range: 0-1, default: 0.6)
--prt-mid                     Output intermediate results during analysis
--help                        Display help information
--method <name>               Analysis method selector (reserved)
--mlma-loco                   Leave-One-Chromosome-Out MLMA (function implemented but
                                not dispatched in option() - partially implemented)
--mem <mb>                    Workspace memory in MB (default: 2048)

============================================================================
DATA TYPE SPECIFICATION
============================================================================
--gene-expression             Specify data as gene expression
--tpm                         Use TPM (Transcripts Per Million) values for gene expression
--methylation                 Specify data as DNA methylation (uses beta values)
--methylation-beta            Explicitly specify beta values for methylation data
--methylation-m               Use M values (logit transform of beta) for methylation data

============================================================================
DATA TRANSFORMATIONS
============================================================================
--m2beta                     Convert M values to beta values during processing
--beta2m                     Convert beta values to M values during processing
--std-probe                  Standardize probes (z-score normalization)
--rint-probe                 Rank-based Inverse Normal Transformation of probes
--no-fid                     Indicate that input files have no family ID column

============================================================================
PROBE / SNP FILTERING & SELECTION
============================================================================
--probe <name>               Target probe name for analysis
--probe-rm <file>            File containing list of probes to remove
--extract-probe <file>       File containing list of probes to extract/keep
--exclude-probe <file>       File containing list of probes to exclude
--from-probe <name>          Starting probe name for range selection
--to-probe <name>            Ending probe name for range selection
--probe-wind <kb>            Probe window size in kilobases (default: 1000)
--from-probe-kb <kb>         Starting probe genomic position in Kb
--to-probe-kb <kb>           Ending probe genomic position in Kb
--extract-snp <file>         File containing list of SNPs to extract/keep
--exclude-snp <file>         File containing list of SNPs to exclude
--snp <name>                 Target SNP name for analysis
--from-snp <name>            Starting SNP name for range selection
--to-snp <name>              Ending SNP name for range selection
--snp-wind <kb>              SNP window size in kilobases (default: 50)
--from-snp-kb <kb>           Starting SNP genomic position in Kb
--to-snp-kb <kb>             Ending SNP genomic position in Kb
--snp-rm <file>              File containing list of SNPs to remove
--chr <n>                    Chromosome number (1-22, X=23, Y=24)
--probe-chr <n>              Filter probes by chromosome
--snp-chr <n>                Filter SNPs by chromosome
--genes <file>               Gene list file (for gene-based probe selection)
--gene <name>                Gene name (for gene-based probe selection)

============================================================================
QUALITY CONTROL THRESHOLDS
============================================================================
--maf <val>                  Minimum minor allele frequency (range: 0-0.5)
--call <val>                 Minimum call rate / genotype rate (range: 0-1)
--sd-min <val>               Minimum standard deviation for probes (range: 0-1)
--missing-ratio-probe <val>  Maximum missing data ratio for probes (range: 0-1, default: 1.0)
--missing-ratio-indi <val>   Maximum missing data ratio for individuals (range: 0-1, default: 1.0)
--zero-ratio-probe <val>     Maximum zero value ratio for probes (range: 0-1)
--detection-pval-file <file> Detection p-value file (for methylation QC)
--dpval-thresh <val>         Detection p-value threshold (range: 0-1, default: 0.05)
--ratio-probe <val>          Ratio threshold for probes (range: 0-1)
--ratio-sample <val>         Ratio threshold for samples (range: 0-1)
--dpval-mth <n>              Detection p-value filtering method (0 or 1)
--impute-mean                Impute missing values with probe mean
--upper-beta <val>           Upper beta threshold for methylation (range: 0-1)
--lower-beta <val>           Lower beta threshold for methylation (range: 0-1)
--lxpo <val>                 Percentage of top probes to exclude from ORM (range: 0-100)
--ld-rsq <val>               LD R-squared threshold (range: 0-1)

============================================================================
RELATIONSHIP MATRICES (ORM/GRM)
============================================================================
--make-orm                   Create ORM in binary format (.orm.bin)
--make-orm-bin               Same as --make-orm (binary format)
--make-orm-gz                Create ORM in gzipped format (.orm.gz)
--orm <prefix>               Input ORM file prefix (binary format)
--orm-bin <prefix>           Same as --orm (binary format)
--grm <prefix>               Input GRM file prefix
--grm-bin <prefix>           Same as --grm (binary format)
--subtract-orm <prefix>      ORM file to subtract (for residual ORM)
--multi-orm <prefix>         Multi-ORM file (for multi-component ORM)
--orm-alg <n>                ORM computation algorithm:
                                1 = standardize probes (default)
                                2 = center probes
                                3 = standardize individuals
--orm-cutoff <val>           ORM cutoff value (for filtering extreme values)
--orm-cutoff-2sides          Apply ORM cutoff on both sides of distribution

============================================================================
REML (Restricted Maximum Likelihood)
============================================================================
--reml                       Perform REML variance component analysis
--reml-priors <vals>         Specify initial variance component values (comma-separated)
--reml-priors-var <vals>     Specify variance priors (alias for --reml-fixed-var)
--reml-fixed-var <vals>      Fix variance components to specified values
--reml-alg <n>               REML algorithm: 0=AI (Average Information), 1=EM, 2=hybrid
--reml-no-constrain          Do not constrain variance components to be positive
--reml-maxit <n>             Maximum number of REML iterations (range: 1-100000, default: 100)
--reml-bendV                 Use bended V matrix (for numerical stability)
--reml-force-converge        Force REML to converge (strict convergence criterion)
--reml-allow-no-converge     Allow analysis to proceed even if REML does not converge
--reml-pred-rand             Predict random effects (BLUP) after REML
--reml-est-fix               Estimate fixed effects after REML
--reml-no-lrt                Do not perform likelihood ratio test
--reml-wfam                  REML within-family analysis
--reml-bivar-nocove           Bivariate REML without covariance estimation
--reml-bivar-no-constrain    Bivariate REML without constraint
--prevalence <val>           Disease prevalence for liability transformation (range: 0-1)
--no-preadj-covar            Do not pre-adjust for covariates (adjust in REML instead)

============================================================================
ASSOCIATION ANALYSIS FLAGS
============================================================================
--linear                     Linear regression analysis (probe-SNP or probe-phenotype)
--logistic                   Logistic regression analysis (for binary phenotypes)
--assoc                      Basic association analysis (no covariate adjustment)
--mlma                       Mixed linear model association (MLMA)
                                Accounts for population structure and relatedness via ORM
--moa                        MOA (Moment of Association)
                                Efficient mixed-model method using moment matching
--moa-exact                  Exact MOA (exact moment calculations instead of approximate)
--moment                     Moment-based analysis
--moment-exact               Exact moment analysis
--moment2-beta               Second-order moment with beta approximation
--vqtl                       Variance QTL analysis
                                Identifies genetic variants affecting phenotypic variance
--eqtl                       eQTL analysis (identifies SNPs associated with expression)
--mlm                        eQTL analysis with mixed linear model
--sqtl                       sQTL analysis (identifies SNPs associated with splicing)

ASSOCIATION ANALYSIS PARAMETERS:
--moment-wind <kb>           Window size for moment analysis in Kb (default: 100)
--moment-num <n>             Maximum number of probes in significant set (default: all)
--moment-alt-pcs <n>         Number of alternative PCs for moment analysis (default: 32)
--moment-percent <val>       Percentage threshold for moment (range: 0-1)
--moment-prior               Use prior information in moment analysis
--moment-force               Force moment analysis (skip alternatives)
--moment-cor                 Use moment correlation (Baptiste method)
--moment-r2 <val>            R-squared threshold for moment (range: 0-1)
--cor-r2 <val>               Correlation R-squared threshold (range: 0-1, default: 0.6)
--force-mlm                  Force MLM (do not switch to linear regression when appropriate)
--fast-linear                Use fast linear method for association
--no-fast-linear             Disable fast linear method
--reverse-assoc              Reverse association direction
--fdr                        Apply false discovery rate correction
--vqtl-mtd <method>          vQTL method:
                                Bartlett, Levene_mean, Levene_median, Fligner_Killeen,
                                drm (Deviation Regression Model), svlm (Squared Value Linear Model)
--adj-probe                  Adjust probe values before analysis
--output-residual            Output residual values

============================================================================
eQTL / sQTL SPECIFIC FLAGS
============================================================================
--cis                        Perform cis analysis (SNP-probe pairs within window)
--cis-wind <kb>              cis window size in Kb (default: 2000)
--trans                      Perform trans analysis (SNP-probe pairs beyond window)
--trans-wind <kb>            trans window size in Kb (default: 5000)
--trans-meta                 trans meta-analysis
--no-isoform-eQTL           Exclude isoform eQTL from analysis
--permutation                Perform permutation testing
--permu-times <n>            Number of permutations (default: 100)

============================================================================
BESD (Binary eQTL Summary Data) FLAGS
============================================================================
--make-besd                  Create BESD file from eQTL summary data
--make-besd-dense            Create dense BESD file
--besd-shrink                Shrink BESD file (remove null associations)
--to-smr                     Convert BESD to SMR format
--query [pval]               Query BESD database for significant associations
                                (default p-value threshold: 5e-8)
--beqtl-summary <file>       BESD summary file (can specify twice for two files)
--besd-flist <file>          File listing multiple BESD files for meta-analysis
--diff                       Compare two BESD files
--befile-flist               Merge multiple BESD files

============================================================================
META-ANALYSIS FLAGS
============================================================================
--meta                       Traditional inverse-variance weighted meta-analysis
--mecs                       MeCS (Meta-analysis of cis-eQTL Summary statistics)
--pmecs <val>                P-value threshold for MeCS (range: 0-1, default: 0.01)
--nmecs <n>                  Number of common SNPs for MeCS correlation (default: 100)
--mecs-mth <n>               MeCS method: 0=PCC, 1=estimate correlation
--gwas-flist <file>          File listing GWAS summary statistics for meta-analysis
--ewas-flist <file>          File listing EWAS summary statistics for meta-analysis
--ewas-summary <file>        EWAS summary statistics file
--gc                         Genomic control for EWAS
--cor-mat <file>             Correlation matrix file
--pcc-z                      Use Z-scores for PCC calculation
--pairwise-common            Output pairwise common probes
--all-common                 Output all common probes

============================================================================
SIMULATION FLAGS
============================================================================
--simu-qt                     Simulate quantitative traits
--simu-cc <cases> <controls>  Simulate case-control traits
--simu-causal-loci <file>     File specifying causal loci for simulation
--simu-rsq <val>              Simulated heritability / R-squared (range: 0-1)
--simu-k <val>                Disease prevalence for simulation (range: 0.0001-0.5)
--simu-seed <val>             Random seed for simulation (must be >100)
--simu-eff-mod <n>            Effect model: 0=additive, 1=dominant
--simu-reverse                Reverse simulation (simulate from phenotype to molecular data)
--simu-residual               Simulate residual only
--simu-causal-loci2 <file>    Second set of causal loci (for bivariate simulation)
--simu-rsq2 <val>             Second simulated R-squared (for bivariate simulation)

============================================================================
PCA / REFACTOR / STEPWISE SELECTION
============================================================================
--pca [n]                    PCA: compute and output n principal components (default: 20)
--refactor <n>               Refactor: cell-type deconvolution with n PCs
--celltype-num <n>           Number of cell types for Refactor
--dmr-num <n>                Number of DMRs (Differentially Methylated Regions)
--autosome-num <n>           Number of autosomes (default: 22)
--npcs <n>                   Number of PCs for normalization
--fixed-pc                   Use fixed PCs (include PCs as fixed effects)
--slct-dom-pc               Select dominant PCs (regress phenotype on each PC)
--clustering-mth <n>        Clustering method: 0=Bonferroni, 1=between, 2=0.05
--pthresh <val>             P-value threshold for stepwise selection (range: 0-1)
--pstep <val>               P-value step for stepwise selection (range: 0-1)
--stepwise-fdr <val>        FDR threshold for stepwise selection (range: 0-1)
--stepwise-rsq <val>        R-squared threshold for stepwise (range: 0-1)
--stepwise-logistic         Use logistic regression in stepwise selection
--stepwise-forward          Forward-only stepwise selection
--stepwise-slct             Stepwise selection mode
--bin-num <n>              Number of bins for variance binning
--bin-mth <n>              Binning method: 0=sample size, 1=weight
--hist-break-num <n>       Number of histogram breaks
--num-rand-comp <n>        Number of random components
--feature-slct-mtd <n>     Feature selection method
--approximate-num <n>      Approximate number for moment analysis
--no-prior-var             No prior variance
--lambda-range <val>       Lambda range for moment analysis
--use-top                  Use top probes
--not-use-top              Do not use top probes

============================================================================
DRM/SVLM MODULE FLAGS (vQTL submodule, parsed by Module_vqtl_drm_svlm.c)
============================================================================
Note: These flags are parsed by the DRM/SVLM module's own argument parser.
Some may not be in the main FLAGS_VALID_CK whitelist and could be rejected.
Use --vqtl-mtd drm or --vqtl-mtd svlm to activate the respective module.

--geno <file>               Genotype file prefix (PLINK .bed/.bim/.fam)
--pheno <file>              Phenotype file (text format)
--pheno-bod <file>          Phenotype file in BOD format
--vqtl                      Activate vQTL module
--vqtl-mtd <method>         vQTL method:
                                Bartlett, Levene_mean, Levene_median,
                                Fligner_Killeen, drm, svlm
--thread-num <n>            Number of CPU threads
--start-var <n>             Starting variant index (1-based)
--end-var <n>               Ending variant index
--start-probe <n>           Starting probe index (1-based)
--end-probe <n>             Ending probe index
--task-num <n>              Total number of parallel tasks
--task-id <n>               Current task ID (1-based)
--trans                     Perform trans analysis
--trans-wind <kb>           trans window size in Kb (default: 5000)
--cis                       Perform cis analysis (default: true)
--cis-wind <kb>             cis window size in Kb (default: 2000)
--pthresh <val>             P-value threshold (range: 0-1, default: 0.5)
--mem <mb>                  Workspace memory in MB
--out <prefix>              Output file prefix
--outformat <format>        Output format
--help                      Display help for vQTL module

============================================================================
COMPUTATIONAL CONTROL
============================================================================
--thread-num <n>             Number of CPU threads (default: auto-detect)
--task-num <n>               Total number of parallel tasks (default: 1)
--task-id <n>                Current task ID (1-based, default: 1)
--mem <mb>                   Workspace memory in MB (default: 2048)
--loud                       Verbose output mode
""",

"examples": """
OSCA USAGE EXAMPLES

============================================================================
1. CREATE EFILE FROM RAW DATA
============================================================================
# From text profile data (rows=probes, cols=individuals)
osca --efile raw_data.txt --make-efile --out my_data

# For methylation data (beta values)
osca --efile methylation.txt --methylation --make-efile --out meth_data

# For gene expression data with TPM
osca --efile expression.txt --gene-expression --tpm --make-efile --out expr_data

# From transposed data (rows=individuals, cols=probes)
osca --tefile transposed_data.txt --make-tefile --out my_data

============================================================================
2. QUALITY CONTROL
============================================================================
# Basic QC with MAF and call rate filters
osca --efile my_data --maf 0.01 --call 0.95 --sd-min 0.1 --out qc_data

# Methylation-specific QC with detection p-value
osca --efile meth_data --methylation \
     --detection-pval-file detection_pvals.txt \
     --dpval-thresh 0.01 \
     --impute-mean \
     --out qc_meth

# Get variance and mean statistics
osca --efile my_data --get-variance --get-mean --out stats

============================================================================
3. COMPUTE ORM (Omic Relationship Matrix)
============================================================================
# Standard ORM (binary format)
osca --efile my_data --make-orm --out my_orm

# ORM with specific algorithm (1=standardize probes)
osca --efile my_data --make-orm --orm-alg 1 --out my_orm

# ORM in gzipped format
osca --efile my_data --make-orm-gz --out my_orm

============================================================================
4. PCA / REFACTOR
============================================================================
# PCA with 20 principal components
osca --efile my_data --pca 20 --out pca_result

# Refactor for cell-type deconvolution (10 PCs, 5 cell types)
osca --efile my_data --refactor 10 --celltype-num 5 --out refactor_result

============================================================================
5. ASSOCIATION ANALYSIS
============================================================================
# Linear regression (probe ~ SNP)
osca --befile my_besd --bfile geno_data --linear --out linear_result

# Logistic regression (binary phenotype)
osca --efile my_data --pheno pheno.txt --logistic --out logistic_result

# MLMA (mixed linear model association)
osca --efile my_data --pheno pheno.txt --mlma --out mlma_result

# MOA (Moment of Association) - efficient mixed model
osca --efile my_data --pheno pheno.txt --moa --out moa_result

# With covariates
osca --efile my_data --pheno pheno.txt --mlma \
     --covar covariates.txt --qcovar quant_covariates.txt \
     --out mlma_with_covar

============================================================================
6. eQTL / sQTL ANALYSIS
============================================================================
# eQTL analysis (cis + trans)
osca --efile expr_data --bfile geno_data --eqtl --out eqtl_result

# cis-eQTL only (within 2000Kb window)
osca --efile expr_data --bfile geno_data --eqtl --cis --cis-wind 2000 --out cis_eqtl

# eQTL with mixed linear model
osca --efile expr_data --bfile geno_data --mlm --out mlm_eqtl

# sQTL analysis
osca --efile expr_data --bfile geno_data --sqtl --bed leafcutter.bed --out sqtl_result

============================================================================
7. VARIANCE QTL (vQTL) ANALYSIS
============================================================================
# vQTL with Bartlett's test
osca --efile my_data --bfile geno_data --vqtl --vqtl-mtd Bartlett --out vqtl_bartlett

# vQTL with DRM (Deviation Regression Model)
osca --efile my_data --bfile geno_data --vqtl --vqtl-mtd drm --out vqtl_drm

# vQTL with SVLM (Squared Value Linear Model)
osca --efile my_data --bfile geno_data --vqtl --vqtl-mtd svlm --out vqtl_svlm

============================================================================
8. REML VARIANCE COMPONENT ANALYSIS
============================================================================
# Basic REML
osca --efile my_data --pheno pheno.txt --reml --out reml_result

# REML with predicted random effects
osca --efile my_data --pheno pheno.txt --reml --reml-pred-rand --out reml_blup

# REML with fixed variance components
osca --efile my_data --pheno pheno.txt --reml --reml-fixed-var 0.5,0.5 --out reml_fixed

============================================================================
9. BESD FILE OPERATIONS
============================================================================
# Create BESD file from eQTL summary data
osca --make-besd --beqtl-summary eqtl_summary.txt --out my_besd

# Query BESD database
osca --befile my_besd --query 5e-8 --out query_result

# Merge multiple BESD files
osca --befile-flist besd_file_list.txt --out merged_besd

# Meta-analysis of BESD files
osca --besd-flist besd_file_list.txt --meta --out meta_result

# MeCS meta-analysis
osca --besd-flist besd_file_list.txt --mecs --pmecs 0.01 --out mecs_result

============================================================================
10. SIMULATION
============================================================================
# Simulate quantitative traits with 10% heritability
osca --efile my_data --simu-qt --simu-rsq 0.1 --simu-causal-loci causal.txt --out simu_qt

# Simulate case-control (1000 cases, 1000 controls)
osca --efile my_data --simu-cc 1000 1000 --simu-rsq 0.1 --simu-k 0.1 \
     --simu-causal-loci causal.txt --out simu_cc

============================================================================
11. MULTI-TASK PARALLEL EXECUTION
============================================================================
# Split analysis into 4 parallel tasks (run with --task-id 1, 2, 3, 4)
osca --efile my_data --mlma --task-num 4 --task-id 1 --out mlma_task1
osca --efile my_data --mlma --task-num 4 --task-id 2 --out mlma_task2
osca --efile my_data --mlma --task-num 4 --task-id 3 --out mlma_task3
osca --efile my_data --mlma --task-num 4 --task-id 4 --out mlma_task4
""",

"formats": """
OSCA DATA FORMAT REFERENCE

============================================================================
1. EFILE FORMAT (OSCA Native Omics Data)
============================================================================
An EFile consists of three files with the same prefix:

  <prefix>.epi  - Probe information file
  <prefix>.eii  - Individual/sample information file
  <prefix>.eed  - Binary data matrix (probe-major, individuals adjacent)

.epi file format (tab/space-delimited, one probe per line):
  Chromosome  ProbeID  GenomicDistance  GeneID  Orientation
  Example: 1  cg00000029  10565  A_23_P133496  -

.eii file format (tab/space-delimited, one individual per line):
  FamilyID  IndividualID  ParentalID  MaternalID  Sex  Phenotype
  Example: FAM1  IND1  0  0  1  -9

.eed file format (binary):
  Header: 16 reserved integers (4 bytes each)
    - [0]: indicator (0=dense full, 1=dense belt, 2=sparse full, 3=sparse belt)
    - [1]: sample size
    - [2]: probe number
    - [3]: value type (0=VALUE, 1=BETAVALUE, 2=MVALUE, 3=TPM)
    - [4-15]: reserved/padding
  Body: float (4-byte) values in probe-major order
    For probe p, individual i: index = p * n_indiv + i

Transposed EFile (.tepi/.teii/.teed):
  Same format but data is individual-major (for memory-efficient access)

============================================================================
2. BOD FORMAT (Binary Omics Data - Compact Storage)
============================================================================
A BOD file set consists of:

  <prefix>.oii  - Individual information file
  <prefix>.opi  - Probe information file
  <prefix>.bod  - Binary data matrix

.oii file format:
  FamilyID  IndividualID  ParentalID  MaternalID  Sex
  Example: FAM1  IND1  0  0  1

.opi file format:
  Chromosome  ProbeID  Position  GeneID  Orientation
  Example: 1  cg00000029  10565  A_23_P133496  -

.bod file format (binary):
  Header: same as .eed (16 integers)
  Body: double (8-byte) values in probe-major order

============================================================================
3. BFILE FORMAT (PLINK Genotype Data)
============================================================================
A BFile consists of three files:

  <prefix>.bed  - Binary genotype matrix
  <prefix>.bim  - SNP information file
  <prefix>.fam  - Family/individual information file

.bed file format (binary):
  Magic number: 0x6c 0x1d (2 bytes)
  Mode: 0x01 = SNP-major (1 byte)
  Body: 2 bits per genotype (00=hom ref, 01=het, 10=hom alt, 11=missing)
    Packed into bytes, individuals rounded up to byte boundary

.bim file format (tab/space-delimited, one SNP per line):
  Chromosome  SNP_ID  GeneticDistance  BP_Position  Allele1  Allele2
  Example: 1  rs1234  0  12345  A  G

.fam file format (tab/space-delimited, one individual per line):
  FamilyID  IndividualID  ParentalID  MaternalID  Sex  Phenotype
  Example: FAM1  IND1  0  0  1  1.5

============================================================================
4. BESD FORMAT (Binary eQTL Summary Data)
============================================================================
A BESD file stores SNP-probe association summary statistics:

  <prefix>.epi  - Probe information (same as EFile)
  <prefix>.esi  - SNP information file
  <prefix>.besd - Binary summary statistics

.esi file format (tab/space-delimited, one SNP per line):
  Chromosome  SNP_ID  BP_Position  Allele1  Allele2
  Example: 1  rs1234  12345  A  G

.besd file format:
  Header: 16 integers
    - [0]: format indicator
    - [1]: sample size
    - [2]: SNP number
    - [3]: probe number
  Body: depends on format:
    Dense:  (beta, se) pairs for each SNP-probe combination
    Sparse: (col_index, beta, se) for non-null associations only

Format indicators:
  SMR_DENSE_1     = 1   (dense, SMR format)
  SMR_SPARSE_3F   = 2   (sparse, SMR format)
  OSCA_SPARSE_1   = 3   (sparse, OSCA format)
  OSCA_DENSE_1    = 4   (dense, OSCA format)

============================================================================
5. ORM / GRM FORMAT (Relationship Matrices)
============================================================================
ORM (Omic Relationship Matrix) and GRM (Genomic Relationship Matrix)
use the same binary format:

  <prefix>.orm.bin  - Binary matrix data (or .grm.bin)
  <prefix>.orm.id   - Individual IDs (or .grm.id)

.orm.bin file format (binary):
  Body: float (4-byte) values representing the lower triangle of the
  relationship matrix (including diagonal), stored row by row

.orm.id file format (tab/space-delimited, one individual per line):
  FamilyID  IndividualID
  Example: FAM1  IND1

Gzipped variant:
  <prefix>.orm.gz   - Gzipped binary matrix (same internal format as .orm.bin)
  <prefix>.orm.id   - Individual IDs (same as above)

============================================================================
6. OUTPUT FILE FORMATS
============================================================================
OSCA generates various output files depending on the analysis:

.ma file (association results):
  Chr  ProbeID  BP  Gene  Orientation  Effect  SE  P_value
  (tab-delimited, one probe per line)

.pca file (PCA results):
  Principal component scores for each individual

.orm.bin / .orm.id (ORM output):
  Binary relationship matrix and individual IDs

.hsq file (REML output):
  Variance component estimates and standard errors

.profile file (score output):
  Polygenic scores for each individual

.log file:
  Detailed analysis log including all parameters and results
"""
}


# ============================================================================
# MCP Tools
# ============================================================================

@mcp.tool()
def osca_help(topic: str = "overview") -> str:
    """Get comprehensive documentation about OSCA commands, flags, and usage.

    Call this tool to learn about OSCA's capabilities before constructing commands.
    Available topics:
      - "overview":     General overview of OSCA and its capabilities
      - "commands":     List of all OSCA command categories and what they do
      - "flags":        Complete reference of all OSCA command-line flags with descriptions
      - "examples":     Usage examples for common OSCA workflows
      - "formats":      Description of all data formats (EFile, BOD, BFile, BESD, ORM/GRM)

    Args:
        topic: Documentation topic to retrieve (default: "overview")

    Returns:
        Documentation text for the requested topic
    """
    return OSCA_DOCS.get(topic, f"Unknown topic: '{topic}'.\n\nAvailable topics: {', '.join(OSCA_DOCS.keys())}")


@mcp.tool()
def run_osca(
    args: list[str],
    workdir: str = "",
    timeout: int = 3600,
    env_overrides: dict[str, str] = None,
) -> dict:
    """Run the OSCA binary with specified command-line arguments.

    This is the primary tool for executing any OSCA analysis. Pass the OSCA flags
    as a list of strings. The tool will execute the OSCA binary, capture all output,
    and return the results including any output files created.

    Examples:
        # Create an ORM from methylation data
        run_osca(["--efile", "meth_data", "--methylation", "--make-orm", "--out", "result"])

        # Run MLMA association analysis with covariates
        run_osca(["--efile", "data", "--pheno", "pheno.txt", "--mlma",
                  "--covar", "cov.txt", "--out", "mlma_result"])

        # Run eQTL analysis
        run_osca(["--efile", "expr", "--bfile", "geno", "--eqtl", "--out", "eqtl"])

    Args:
        args: List of OSCA command-line arguments (e.g., ["--efile", "data", "--make-orm"])
        workdir: Working directory for OSCA execution (default: current directory).
                 All input files should be relative to this directory,
                 and all output files will be created in this directory.
        timeout: Maximum execution time in seconds (default: 3600 = 1 hour).
                 Long-running analyses like eQTL or PCA may need more time.
        env_overrides: Optional environment variable overrides (e.g., {"OMP_NUM_THREADS": "4"})

    Returns:
        dict with keys:
          - command: The full command that was executed
          - exit_code: Process exit code (0 = success)
          - stdout: Standard output from OSCA
          - stderr: Standard error from OSCA
          - execution_time_sec: Wall-clock execution time
          - workdir: Working directory used
          - output_files: List of files created/modified during execution
          - log_content: Contents of the OSCA log file (if found)
          - error: Error message if the command could not be executed
    """
    result = {
        "command": "",
        "exit_code": None,
        "stdout": "",
        "stderr": "",
        "execution_time_sec": 0,
        "workdir": workdir or str(Path.cwd()),
        "output_files": [],
        "log_content": "",
        "error": "",
    }

    # Validate OSCA binary
    if not OSCA_BIN.exists():
        result["error"] = (
            f"OSCA binary not found at {OSCA_BIN}. "
            f"Ensure the 'osca' executable is in the same directory as this MCP server script ({SCRIPT_DIR})."
        )
        return result

    if not os.access(OSCA_BIN, os.X_OK):
        result["error"] = (
            f"OSCA binary at {OSCA_BIN} is not executable. "
            f"Run: chmod +x {OSCA_BIN}"
        )
        return result

    # Check platform compatibility
    current_platform = platform.system()
    if current_platform == "Darwin":
        # On macOS, the Linux binary won't run directly
        result["error"] = (
            f"OSCA binary is a Linux x86_64 executable but the current platform is macOS ({current_platform}). "
            f"OSCA can only be executed on Linux. Consider running this MCP server on a Linux machine, "
            f"or use a Linux container/VM."
        )
        return result

    # Build command
    cmd = [str(OSCA_BIN)] + [str(a) for a in args]
    result["command"] = " ".join(cmd)

    # Determine output prefix for log file detection
    out_prefix = "osca"
    for i, a in enumerate(args):
        if a == "--out" and i + 1 < len(args):
            out_prefix = args[i + 1]
            break

    # Snapshot files before execution (to detect new/modified files)
    workdir_path = Path(workdir) if workdir else Path.cwd()
    if not workdir_path.exists():
        result["error"] = f"Working directory does not exist: {workdir_path}"
        return result

    files_before = set()
    for f in workdir_path.rglob("*"):
        if f.is_file():
            files_before.add(f)

    # Prepare environment
    run_env = os.environ.copy()
    if env_overrides:
        run_env.update(env_overrides)

    # Execute OSCA
    try:
        start_time = time.time()
        proc = subprocess.run(
            cmd,
            cwd=str(workdir_path) if workdir else None,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=run_env,
        )
        elapsed = time.time() - start_time

        result["exit_code"] = proc.returncode
        result["stdout"] = proc.stdout[:50000] if proc.stdout else ""
        result["stderr"] = proc.stderr[:50000] if proc.stderr else ""
        result["execution_time_sec"] = round(elapsed, 2)

        if proc.returncode != 0:
            result["error"] = f"OSCA exited with code {proc.returncode}. Check stderr for details."

    except subprocess.TimeoutExpired:
        result["error"] = f"OSCA execution timed out after {timeout} seconds."
        result["exit_code"] = -1
        return result
    except FileNotFoundError as e:
        result["error"] = f"Failed to execute OSCA binary: {e}"
        result["exit_code"] = -1
        return result
    except Exception as e:
        result["error"] = f"Unexpected error during OSCA execution: {e}"
        result["exit_code"] = -1
        return result

    # Detect output files (new or modified files)
    files_after = set()
    for f in workdir_path.rglob("*"):
        if f.is_file():
            files_after.add(f)

    new_or_modified = sorted(files_after - files_before, key=lambda p: p.name)
    result["output_files"] = [str(f.relative_to(workdir_path)) for f in new_or_modified]

    # Try to read the OSCA log file
    # Log file naming: <out_prefix>_1_1.log or osca.log
    possible_log_files = [
        workdir_path / f"{out_prefix}_1_1.log",
        workdir_path / "osca.log",
        workdir_path / f"{out_prefix}.log",
    ]

    # Also check if --out contains a directory path
    out_dir = Path(out_prefix).parent
    if str(out_dir) != ".":
        possible_log_files.append(workdir_path / out_dir / f"{Path(out_prefix).name}_1_1.log")
        possible_log_files.append(workdir_path / out_dir / "osca.log")

    for log_path in possible_log_files:
        if log_path.exists():
            try:
                log_text = log_path.read_text(errors="replace")
                result["log_content"] = log_text[:50000]
                break
            except Exception:
                pass

    return result


@mcp.tool()
def list_files(
    path: str = ".",
    pattern: str = "*",
    recursive: bool = False,
    include_size: bool = True,
) -> list[dict]:
    """List files in a directory, optionally matching a glob pattern.

    Useful for checking what OSCA output files were created, examining input
    file structure, or navigating the file system.

    Args:
        path: Directory path to list files from (default: current directory)
        pattern: Glob pattern to match files (default: "*" = all files)
                 Examples: "*.ma", "*orm*", "*.besd", "*.log"
        recursive: If True, search recursively in subdirectories (default: False)
        include_size: If True, include file size in bytes (default: True)

    Returns:
        List of dicts, each with keys:
          - name: File name
          - path: Full relative path
          - size_bytes: File size in bytes (if include_size=True)
          - size_human: Human-readable file size (if include_size=True)
          - modified: Last modification time (ISO format)
    """
    dir_path = Path(path)

    if not dir_path.exists():
        return [{"error": f"Path does not exist: {path}"}]

    if not dir_path.is_dir():
        return [{"error": f"Path is not a directory: {path}"}]

    results = []

    if recursive:
        search_path = dir_path / "**" / pattern
        files = sorted(dir_path.rglob(pattern), key=lambda p: p.name)
    else:
        files = sorted(dir_path.glob(pattern), key=lambda p: p.name)

    for f in files:
        if not f.is_file():
            continue

        info = {
            "name": f.name,
            "path": str(f),
        }

        if include_size:
            stat = f.stat()
            info["size_bytes"] = stat.st_size
            info["size_human"] = _format_size(stat.st_size)
            info["modified"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stat.st_mtime))

        results.append(info)

    return results


@mcp.tool()
def read_file(
    path: str,
    max_lines: int = 200,
    offset: int = 0,
    max_bytes: int = 51200,
) -> dict:
    """Read the contents of a text file, with support for pagination.

    Essential for inspecting OSCA output files such as .ma (association results),
    .hsq (REML results), .log (analysis log), or any input/output file.

    Args:
        path: Path to the file to read
        max_lines: Maximum number of lines to return (default: 200)
        offset: Line number to start reading from (0-indexed, default: 0)
        max_bytes: Maximum total bytes to read (default: 51200 = 50KB)

    Returns:
        dict with keys:
          - path: File path
          - content: File contents (truncated to max_lines and max_bytes)
          - total_lines: Total number of lines in the file
          - lines_returned: Number of lines actually returned
          - offset: Starting line offset used
          - truncated: Whether output was truncated
          - error: Error message if file could not be read
    """
    file_path = Path(path)

    if not file_path.exists():
        return {"error": f"File does not exist: {path}"}

    if not file_path.is_file():
        return {"error": f"Path is not a file: {path}"}

    try:
        # Read all lines
        with open(file_path, "r", errors="replace") as f:
            all_lines = f.readlines()

        total_lines = len(all_lines)

        # Apply offset and max_lines
        end_idx = offset + max_lines
        selected_lines = all_lines[offset:end_idx]

        # Join and truncate to max_bytes
        content = "".join(selected_lines)
        truncated = False

        if len(content) > max_bytes:
            content = content[:max_bytes]
            truncated = True

        if end_idx < total_lines:
            truncated = True

        return {
            "path": str(file_path),
            "content": content,
            "total_lines": total_lines,
            "lines_returned": len(selected_lines),
            "offset": offset,
            "truncated": truncated,
        }

    except Exception as e:
        return {"error": f"Failed to read file: {e}"}


@mcp.tool()
def osca_info() -> dict:
    """Get information about the OSCA binary installation.

    Returns diagnostic information including:
      - Whether the OSCA binary exists and is executable
      - The binary path
      - The OSCA version (if determinable)
      - The current platform
      - The MCP server script path

    Call this tool first to verify the OSCA installation is working correctly.

    Returns:
        dict with keys: binary_path, exists, executable, version, platform,
                        script_dir, mcp_server_path, error
    """
    info = {
        "binary_path": str(OSCA_BIN),
        "exists": OSCA_BIN.exists(),
        "executable": os.access(OSCA_BIN, os.X_OK) if OSCA_BIN.exists() else False,
        "version": "v1.22",
        "platform": platform.system(),
        "platform_machine": platform.machine(),
        "script_dir": str(SCRIPT_DIR),
        "mcp_server_path": str(SCRIPT_DIR / "mcp_server.py"),
        "error": "",
    }

    if not OSCA_BIN.exists():
        info["error"] = f"OSCA binary not found at {OSCA_BIN}."
    elif not info["executable"]:
        info["error"] = f"OSCA binary is not executable. Run: chmod +x {OSCA_BIN}"

    return info


# ============================================================================
# Helper Functions
# ============================================================================

def _format_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size = float(size_bytes)

    while size >= 1024 and i < len(size_names) - 1:
        size /= 1024
        i += 1

    return f"{size:.1f} {size_names[i]}"


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    mcp.run()
