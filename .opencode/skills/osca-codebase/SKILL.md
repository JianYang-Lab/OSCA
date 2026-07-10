---
name: osca-codebase
description: Guide to the OSCA (OmicS-data-based Complex trait Analysis) C++ codebase. Use when working with files under src/, lib/, or the root build files (Makefile, CMakeLists.txt), when adding/modifying command-line flags or analysis functions, or when navigating the layered l0-l4 architecture.
---

# OSCA Codebase Skill

## Project Identity

OSCA (OmicS-data-based Complex trait Analysis) is a C++ command-line tool for analyzing complex traits using multi-omics data (methylation, gene expression) and performing genetic analysis of molecular phenotypes. Developed by Yang Lab, Westlake University. Current version: v1.22.

- Entry point: `main()` in `src/l4_osc.cpp:33`
- Build files: `Makefile`, `CMakeLists.txt`
- Language: C++11 (with some C modules)
- External libs: Eigen, Intel MKL, Rmath, GSL, zlib, OpenMP

## Layered Architecture

The source code in `src/` is organized into numbered layers (l0-l4), each building on the one below:

### Layer 0 — Base Utilities
- `l0_com.h/.cpp` — Common globals, macros (`LOGPRINTF`, `CACHEALIGN`), string/IO helpers, `logprintb()`, `TERMINATE()`. Defines workspace constants and the `wkspace_base` pointer.
- `l0_io.h/.cpp` — Low-level file I/O wrappers, `fopen_checked()`, `FileExist()`, `split_string()`.
- `l0_mem.h/.cpp` — Workspace memory allocator (`wkspace_base`, `wkspace_left`), `getMemSize_Plink()`, `getAllocMB_Plink()`.
- `l0_stat.h/.cpp` — Statistical primitives: `cor()`, `var()`, `mean()`, `standardise()`, `inverse_V()`, rank templates.

### Layer 1 — Genotype Operations & Statistics
- `l1_op_geno.h/.cpp` — Genotype matrix operations, LD calculation (`_calc_ld()`), `make_XMat()`.
- `l1_stat.h/.hpp` — Higher-level statistics for genotype/phenotype analysis.

### Layer 2 — File Formats, Kernels & REML
- `l2_bfile.h/.cpp` (namespace `BFILE`) — PLINK BED/BIM/FAM reader/writer. Key struct: `bInfo` (genotype data, SNP info, family structure, GRM, REML state). Functions: `read_famfile()`, `read_bimfile()`, `read_bedfile()`, `make_grm()`, `make_XMat()`, `testLinear()`, `testLogit()`, `stepwise_slct()`.
- `l2_efile.h/.cpp` (namespace `EFILE`) — EFile format (epi/eii/eed) for omics data. Key struct: `eInfo` (probe info, individual info, values, GRM, REML state). Functions: `read_efile()`, `read_efile_t()`, `read_eii()`, `read_epi()`, `make_erm()`, `load_workspace()`, `cal_var_mean()`, `rintprobe()`, `stdprobe()`.
- `l2_besd.hpp/.cpp` (namespace `SMR`) — BESD (Binary eQTL Summary Data) format. Key struct: `eqtlInfo` (SNP/probe indices, beta/se values, sparse/dense storage). Defines BESD format constants: `SMR_DENSE_1`, `SMR_SPARSE_3F`, `OSCA_SPARSE_1`, `OSCA_DENSE_1`.
- `l2_reml.h/.cpp` (namespace `EFILE`) — REML (Restricted Maximum Likelihood) estimation. Functions: `reml()` (3 overloads), `calcu_Vi()`, `mlma_calcu_stat()`, `mlma_calcu_stat_covar()`, `blup_probe_geno()`.
- `l2_enet.hpp/.cpp` — Elastic Net regression for probe selection.

### Layer 3 — Analysis Pipelines
- `l3_efile.h/.cpp` (namespace `EFILE`) — Top-level EFile operations: `merge_beed()`, `make_bld()`, `make_beed()`, `make_efile()`, `make_erm()`, `mlma()`, `mlma_loco()`, `pca()`, `assoc()`, `linear()`, `logistic()`, `fit_reml()`, `EWAS_simu()`, `scoreIndividuals()`, `blup_probe()`, `getPrbVarianceMean()`.
- `l3_gwas.hpp/.cpp` (namespace `BFILE`) — GWAS analysis: `moment_gwas()` (MOA for GWAS), `mlm_cal_stat()`, `mlm_cal_stat_covar()`.
- `l3_ewas.hpp/.cpp` (namespace `EFILE`) — EWAS analysis: `moment()` (MOA), `moment_exact()` (exact MOA).
- `l3_smr.hpp/.cpp` (namespace `SMR`) — SMR (Summary-based Mendelian Randomization) analysis: `query_besd()`, `make_besd()`, `meta()`, `meta_gwas()`, `gc_ewas()`.
- `l3_vqtl.hpp/.cpp` (namespace `VQTL`) — Variance QTL analysis: `V_QTL()`, `eQTL()`, `eQTL_MLM()`, `sQTL()`, `ssQTL()`.
- `l3_permutation.hpp/.cpp` (namespace `PERMU`) — Permutation testing for sQTL: `permu_sqtl()`.
- `l3_glmnet.cpp` — GLMnet wrapper for elastic net.

### Layer 4 — Orchestrator
- `l4_osc.h/.cpp` — Main entry point. Contains:
  - `main()` (`l4_osc.cpp:33`): Sets up log file, allocates 2GB workspace, calls `option()`.
  - `option()` (`l4_osc.cpp:133`): Parses all `--*` flags, validates with `FLAGS_VALID_CK()`, dispatches to analysis functions.
  - `FLAGS_VALID_CK()` (`l4_osc.h:27`): Validates all command-line flags against a whitelist.

## Special Modules

- `src/Module_vqtl_drm_svlm.h/.c` — Standalone vQTL module with two methods:
  - **DRM** (Deviation Regression Model): C implementation of DRM (originally R, from https://github.com/drewmard/DRM). See https://doi.org/10.1016/j.ajhg.2020.11.016.
  - **SVLM** (Squared residual Value Linear Modeling): From VariABEL R package. See https://bmcgenomdata.biomedcentral.com/articles/10.1186/1471-2156-13-4.
  - Entry points: `Module_vqtl_drm()`, `Module_vqtl_svlm()` — dispatched directly from `main()` before `option()` if `--drm` or `--svlm` flags are set.
- `src/cis_learn_beta.hpp/.cpp` — Learns beta distribution parameters for p-value correction (copied from qtltools). Function: `learnBetaParameters()`.
- `src/dcdflib.cpp/.h` + `src/ipmpar.h` — DCDFLIB library for computing cumulative distribution functions and inverses (used for chi-square, F, beta distributions).

## Library Layer (`lib/`)

- `lib/besdfile.h/.c` — Low-level BESD file I/O: `besd_sparse_write_meta()`, `besd_sparse_write_variant_index()`, `besd_sparse_write_beta_se_data()`.
- `lib/bodfile.h/.c` — BOD (Binary Omics Data) file format. Struct: `BODFILE` (individual_num, probe_num, file pointers, offsets). Supports `.oii` (individual info), `.opi` (probe info), `.bod` (data) files. Functions: `bodfileopen()`, `bodfileclose()`, `oiireadline()`, `opireadline()`, `bodreaddata()`, `bodloaddata_n()`, `bodloaddata_all()`.
- `lib/plinklite.h/.c` — Lightweight PLINK BED file reader. Struct: `PLINKFILE` (individual_num, variant_num, file pointers, buffers). Functions: `plinkopen()`, `plinkclose()`, `famreadline()`, `bimreadline()`, `bedreaddata()`, `bedloaddata_n()`, `bedloaddata_all()`.
- `lib/sysinfo.h/.c` — System information utilities.
- `lib/CMakeLists.txt` — Builds `oscalib` static library from `besdfile.c`, `bodfile.c`, `plinklite.c`, `sysinfo.c`.

## Data Formats

### BFile (PLINK format)
- `.bed` — Binary genotype data (major allele count per individual)
- `.bim` — SNP info: chrom, rsid, genetic distance, bp, allele1, allele2
- `.fam` — Individual info: family_id, within_famid, father_id, mother_id, sex, phenotype

### EFile (Omics data)
- `.epi` — Probe info: chrom, probe_id, position, gene_id, orientation
- `.eii` — Individual info: family_id, indiv_id, parental_id, maternal_id, sex, phenotype
- `.eed` — Values matrix (probe major, individuals adjacent)
- Transposed variant: `.tepi`/`.teii`/`.teed` (individual major)

### BESD (Binary eQTL Summary Data)
- Stores SNP-probe associations (beta, SE) in sparse or dense format
- Header: 16 reserved ints (indicator + sample_size + snp_number + probe_number + padding)
- Sparse: additional `val_number`, `cols`, `rowid`, `betases`
- Dense: `<beta, se>` pairs for each SNP across all probes

### BOD (Binary Omics Data)
- `.oii` — Individual info (family_id, indiv_id, parental_id, maternal_id, sex)
- `.opi` — Probe info (chrom, probe_id, position, gene_id, orientation)
- `.bod` — Data matrix (double values)

### ORM/GRM (Relationship Matrices)
- **ORM** (Omic Relationship Matrix) — Computed from omics data
- **GRM** (Genomic Relationship Matrix) — Computed from genotype data
- Binary format: `.orm.bin`/`.grm.bin` + `.orm.id`/`.grm.id`
- GZ format: `.orm.gz`/`.grm.gz` + `.orm.id`/`.grm.id`

## Command Dispatch Logic

The `option()` function in `l4_osc.cpp:133` parses all command-line flags and dispatches to analysis functions based on a priority-ordered chain of `if/else if` blocks. The dispatch priority (first match wins):

1. `--befile-flist` → `merge_beed()` — Merge multiple BESD files
2. `--make-bod` → `make_beed()` — Create BOD file from EFile
3. `--make-bld` → `make_bld()` — Create BLD file from EFile
4. `--make-efile` / `--make-tefile` → `make_efile()` — Create EFile from text
5. `--make-orm` / `--make-orm-bin` / `--make-orm-gz` → `make_erm()` — Create ORM
6. `--moa-exact` → `moa()` — Exact MOA (mixed linear model analysis)
7. `--moment-exact` → `moment_exact()` — Exact moment analysis
8. `--moment` / `--moment2-beta` → `moment()` or `moment_gwas()` — MOA analysis
9. `--mlma` / `--moa` → `mlma()` — MLMA analysis
10. `--pca` → `pca()` — Principal component analysis
11. `--diff` → `diff()` — Compare two BESD files
12. `--update-opi` → `update_epifile()` — Update probe info file
13. `--refactor` → `getRefactor()` — Refactoring analysis
14. `--assoc` → `assoc()` — Association analysis
15. `--linear` → `linear()` — Linear regression
16. `--logistic` → `logistic()` — Logistic regression
17. `--simu-qt` / `--simu-cc` → `EWAS_simu()` / `EWAS_simu2()` — Simulation
18. `--reml` → `fit_reml()` — REML analysis
19. `--vqtl` → `V_QTL()` — Variance QTL analysis
20. `--eqtl` → `eQTL()` — eQTL analysis
21. `--mlm` → `eQTL_MLM()` — eQTL with MLM
22. `--sqtl` → `sQTL()` / `ssQTL()` / `permu_sqtl()` — sQTL analysis
23. `--query` → `query_besd()` — Query BESD database
24. `--meta` / `--mecs` → `meta()` / `meta_gwas()` — Meta-analysis
25. `--make-besd` → `make_besd()` — Create BESD file
26. `--gc` → `gc_ewas()` — Genomic control for EWAS

## Key Data Structures

### `eInfo` (`src/l2_efile.h:24`)
Main structure for EFile data. Contains:
- `_eType` — Data type (GENEEXPRESSION, METHYLATION, OTHERDATA)
- `_epi_num`, `_epi_chr`, `_epi_prb`, `_epi_gd`, `_epi_bp`, `_epi_gene`, `_epi_orien` — Probe info
- `_eii_num`, `_eii_fid`, `_eii_iid`, `_eii_sex`, `_eii_pheno` — Individual info
- `_val` — Values (probe major)
- `_grm` — Relationship matrix
- `_varcmp`, `_var_name`, `_hsq_name` — REML results
- `_P`, `_b`, `_se` — BLUP and statistical results

### `bInfo` (`src/l2_bfile.h:17`)
Main structure for BFile (PLINK) data. Contains:
- `_chr`, `_snp_name`, `_allele1`, `_allele2`, `_bp` — SNP info
- `_fid`, `_pid`, `_sex`, `_pheno` — Individual info
- `_snp_1`, `_snp_2` — Genotype booleans
- `_geno` — Genotype matrix
- `_grm` — Genomic relationship matrix
- `_varcmp`, `_var_name` — REML results
- `_b`, `_se` — Fixed effect estimates

### `eqtlInfo` (`src/l2_besd.hpp:29`)
Main structure for BESD (eQTL summary) data. Contains:
- `_esi_chr`, `_esi_rs`, `_esi_bp`, `_esi_allele1`, `_esi_allele2` — SNP info
- `_epi_chr`, `_epi_prbID`, `_epi_bp`, `_epi_gene`, `_epi_orien` — Probe info
- `_cols`, `_rowid`, `_val` — Sparse storage
- `_bxz`, `_sexz` — Dense storage (beta/SE matrices)
- `_probNum`, `_snpNum`, `_valNum`, `_sampleNum` — Dimensions

## Build System

### Method 1: Makefile
```bash
make
```
Variables (set via `make VAR=VALUE`):
- `EIGEN_PATH` — Eigen headers (default: `/usr/include`)
- `MKL_INCLUDE` — MKL headers (default: `/usr/include`)
- `MKL_LIB` — MKL libraries (default: `/usr/lib64/intel64`)
- `Rmath_INCLUDE` — Rmath headers (default: `/usr/include`)
- `Rmath_LIB` — Rmath libraries (default: `/usr/lib64/lib`)
- `DEBUG` — Set to enable debug mode (`-g -O0`)

Links against: `-lz -lgomp -lmkl_core -lpthread -lmkl_gnu_thread -lmkl_intel_lp64 -lRmath -lgsl -lgslcblas -luuid`

### Method 2: CMake
```bash
mkdir build && cd build
cmake ..
make
```
CMake features:
- Uses CPM (CMake Package Manager) to download dependencies: zlib 1.3.1, eigen 3.4.0, gsl 2.7.0
- Supports Linux, macOS, and Windows
- On macOS: uses Accelerate framework, OpenMP via homebrew
- On Linux: uses MKL, links against `gomp`, `pthread`, `m`, `dl`, `uuid`
- Options: `BUILD_STATIC`, `CUSTOM_INCLUDE_SEARCH_PATH`, `CUSTOM_LIB_SEARCH_PATH`

### Output
- Dynamic build: `osca` executable
- Static build: `osca_static` executable (Makefile only)

## Dependencies

| Dependency | Purpose | Version |
|------------|---------|---------|
| Eigen | Linear algebra (Matrix, Vector, decompositions) | 3.3.7+ (3.4.0 via CPM) |
| Intel MKL | Math kernel library (Linux/Windows) | Latest |
| Rmath | R math library (distribution functions) | 3.6+ |
| GSL | GNU Scientific Library | 2.6+ (2.7.0 via CPM) |
| zlib | Compression | 1.2+ (1.3.1 via CPM) |
| OpenMP | Parallelization | Any |
| libuuid | UUID generation | 1.0.3+ |

## Namespaces

- `EFILE` — EFile operations (l2_efile, l2_reml, l3_efile, l3_ewas)
- `BFILE` — BFile operations (l2_bfile, l3_gwas)
- `SMR` — SMR analysis operations (l2_besd, l3_smr)
- `VQTL` — vQTL analysis operations (l3_vqtl)
- `PERMU` — Permutation operations (l3_permutation)

## Key Constants and Macros

- `OSCA_VERSION` (`src/config.h:4`) — Current version string (`"v1.22"`)
- `MODULE_VQTL_DRM_SVLM` (`src/config.h:10`) — Enables vQTL DRM/SVLM module
- `WKSPACE_DEFAULT_MB` (`src/l0_com.h:51`) — Default workspace size (2048 MB)
- `MAXPROBENUM` (`src/l0_com.h:58`) — Maximum probe count (0x100000, ~1M)
- `MISSING_PHENO` (`src/l0_com.h:61`) — Missing phenotype sentinel (-1e10)
- `MISSING_PROFILE` (`src/l0_com.h:62`) — Missing profile sentinel (1e10)
- `LOGPRINTF(...)` (`src/l0_com.h:72`) — Macro to format and write to log: `sprintf(logbuf, __VA_ARGS__); logprintb();`
- `CACHEALIGN(val)` (`src/l0_com.h:73`) — Align value to cache line (64 bytes)

## Important Implementation Notes

1. **Workspace memory**: OSCA allocates a large contiguous workspace (`wkspace_base`) at startup (default 2GB). Most data structures use this workspace rather than individual `malloc` calls.

2. **Log file**: All output goes through `LOGPRINTF` macro which writes to both `logfile` and stdout. The log file is named `osca.log` by default, or `<outname>_<task_num>_<task_id>.log` if `--out` is specified.

3. **Task parallelism**: OSCA supports splitting analysis across multiple processes via `--task-num` and `--task-id` flags.

4. **Thread parallelism**: OpenMP is used for parallelization. Thread count is set via `--thread-num` (default: `thread_num` from environment).

5. **Flag validation**: All command-line flags are validated against a whitelist in `FLAGS_VALID_CK()` (`src/l4_osc.h:27`). Unknown flags cause termination.

6. **Multiple file format support**: OSCA supports both PLINK BFile format (via `lib/plinklite.c`) and its own EFile/BOD format (via `lib/bodfile.c`). The `l2_efile.h` provides the high-level interface for EFile operations.

7. **Sparse and dense BESD formats**: BESD files can be stored in either sparse (only non-null associations) or dense (all SNP-probe pairs) formats. The format is determined by constants in `l2_besd.hpp`.

8. **MKL vs Accelerate**: On Linux/Windows, OSCA uses Intel MKL for linear algebra. On macOS, it uses the Accelerate framework instead.

## Common Patterns

### Adding a new command-line flag
1. Add the flag string to the whitelist in `FLAGS_VALID_CK()` (`src/l4_osc.h:27`)
2. Add a parsing block in `option()` (`src/l4_osc.cpp:133`) following the existing pattern:
   ```cpp
   if(0==strcmp(option_str[i],"--new-flag")){
       new_var = option_str[++i];
       FLAG_VALID_CK("--new-flag", new_var);
       LOGPRINTF("--new-flag %s\n", new_var);
   }
   ```
3. Add the dispatch logic in the appropriate `if/else if` chain in `option()`.

### Adding a new analysis function
1. Declare the function in the appropriate header (e.g., `l3_efile.h`)
2. Implement the function in the corresponding `.cpp` file
3. Add a dispatch block in `option()` (`src/l4_osc.cpp`)

### File I/O patterns
- Text files: Read line by line using `split_string()` or `split_str()`
- Binary files: Use `fopen_checked()` and `fwrite_checked()` for safe I/O
- PLINK files: Use `plinkopen()`, `famreadline()`, `bimreadline()`, `bedreaddata()`
- BOD files: Use `bodfileopen()`, `oiireadline()`, `opireadline()`, `bodreaddata()`
- BESD files: Use functions from `l2_besd.hpp`

## Testing

No formal test suite exists in the repository. Testing is typically done via:
- Running OSCA with example datasets
- Comparing output against known results
- The official documentation at https://yanglab.westlake.edu.cn/software/osca/ provides usage examples

## Lint and Typecheck Commands

- **Lint**: No linting configuration found. Consider using `clang-tidy` or `cppcheck`.
- **Typecheck**: C++ compilation serves as type checking. Use:
  ```bash
  make  # or
  cd build && cmake --build .
  ```

## Code Style

- Indentation: 4 spaces
- Naming: snake_case for functions and variables, CamelCase for some structs
- Headers: `.h` for C headers, `.hpp` for C++ headers, `.cpp` for implementations
- Namespaces: Used extensively (`EFILE`, `BFILE`, `SMR`, `VQTL`, `PERMU`)
- Error handling: `LOGPRINTF` for errors, `TERMINATE()` for fatal errors
- Memory management: Mix of `malloc`/`free` for workspace and `new`/`delete` for objects

## File Dependencies (Include Graph)

```
l4_osc.h
├── l3_vqtl.hpp
│   ├── l2_efile.h → l1_op_geno.h, l1_stat.hpp
│   ├── l2_bfile.h → l1_op_geno.h, l2_efile.h
│   ├── l2_reml.h → l2_efile.h, l0_stat.h
│   └── l2_besd.hpp → l2_efile.h, l2_bfile.h, l2_reml.h
├── l3_smr.hpp → l2_besd.hpp
├── l3_ewas.hpp → l3_efile.h
├── l3_efile.h → l2_efile.h, l2_reml.h, l2_bfile.h
├── l3_gwas.hpp → l2_reml.h, l2_bfile.h
├── l3_permutation.hpp → l2_efile.h, l2_bfile.h, l2_reml.h, l2_besd.hpp, l3_vqtl.hpp
└── Module_vqtl_drm_svlm.h
```

## Key Files Reference

| File | Purpose | Key Functions |
|------|---------|---------------|
| `src/l4_osc.cpp` | Main orchestrator | `main()`, `option()` |
| `src/l0_com.h` | Common definitions | `LOGPRINTF`, `TERMINATE()` |
| `src/l0_mem.cpp` | Memory management | `wkspace_alloc()`, `wkspace_free()` |
| `src/l2_efile.h` | EFile data structure | `eInfo`, `read_efile()`, `make_erm()` |
| `src/l2_bfile.h` | BFile data structure | `bInfo`, `read_famfile()`, `make_grm()` |
| `src/l2_besd.hpp` | BESD format | `eqtlInfo`, format constants |
| `src/l2_reml.h` | REML estimation | `reml()`, `calcu_Vi()` |
| `src/l3_efile.h` | EFile operations | `mlma()`, `pca()`, `assoc()`, `linear()` |
| `src/l3_vqtl.hpp` | vQTL operations | `V_QTL()`, `eQTL()`, `sQTL()` |
| `src/l3_smr.hpp` | SMR operations | `query_besd()`, `make_besd()`, `meta()` |
| `lib/plinklite.h` | PLINK reader | `plinkopen()`, `famreadline()` |
| `lib/bodfile.h` | BOD reader | `bodfileopen()`, `bodreaddata()` |
| `lib/besdfile.h` | BESD writer | `besd_sparse_write_meta()` |
