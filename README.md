# OSCA  

OSCA (OmicS-data-based Complex trait Analysis) is a software tool for the analysis of complex traits using multi-omics data and genetic analysis of molecular phenotypes.

## Requirement

- zlib >= 2.1

- gsl >= 2.6

- Eigen

- MKL(Math Kernel Library)

    MKL is distributed within intel oneAPI, you can get this by install intel oneAPI or install [oneMKL](https://www.intel.com/content/www/us/en/developer/tools/oneapi/onemkl-download.html) conponent.

- Rmath library

## Instatll requirements

- [Eigen](https://eigen.tuxfamily.org/index.php?title=Main_Page)

    Eigen just contain head files, and do not need compile to install it. Here, we use version 3.3.7 when we compile osca.

- MKL

    You can read document and download MKL at this webpage: https://www.intel.com/content/www/us/en/developer/tools/oneapi/toolkits.html#base-kit.  

- Rmath library

    __Note__: functions of Rmath are also contained by libR.so/libR.a, you can use them instead of Rmath to make life easier.

    I using version 3.6 as example to install this library.

    * download R

        `wget https://cloud.r-project.org/src/base/R-3/R-3.6.3.tar.gz`  
        `tar -zxf R-3.6.3.tar.gz`  
        `cd R-3.6.3`  
    
    * configure

        `./configure --prefix="PATH where you what put this lib"`  
    
    * compile and install

        `cd src/nmath/standalone`  
        `make`  
        `make install`  
    
    Then the head files and library files would show up under prefix path.

## Compile

* Method 1, using Makefile

    Samplely, if all requirements is installed under **/usr**, just run following command, then the **osca** would be compiled.

    ```
    make  
    ```

    This would search head file under `/usr/include` and search library under `/usr/lib64`.  

    If you don't install requirements in other directory, you may need edit Makefile or specific following variables when run `make` command.

    ```
    make EIGEN_PATH="eigen head file path" MKL_INCLUDE="mkl head file path" \
    MKL_LIB="mkl library file path" RMath_INCLUDE="path where install Rmath head files" RMath_LIB="path where install Rmath library"
    ```

    By default, only the dynamic version would compiled, if you want compile static version, run:

    ```
    make VIRABLE="VALUE" osca_static
    ```
    Using `DEBUG=ON` to switch on debug mode.

    After compilation, a file named **osca** would appared under same directory of `Makefile`, and if you compile static version, the executable file, named **osca_static**, would show up too. 


* Method 2, using cmake

    ```
        git clone https://github.com/benjaminfang/osca.git
        cd osca
        mkdir build
        cd build
        cmake ..
        make
    ```

## USAGE

See https://yanglab.westlake.edu.cn/software/osca/#Overview for its usage and data resources.

## MCP Server — Use OSCA via AI Conversation

The pre-built binary directory (`osca-1.22-linux-x86_64/`) ships with an MCP
server (`mcp_server.py`) that exposes all OSCA functionality to AI assistants
such as **Claude Desktop**, **OpenAI Codex**, and **opencode**.

### Quick Start

```bash
pip install mcp
```

Add the server to your AI tool's config (replace `<OSCA_DIR>` with the real path to the `osca-1.22-linux-x86_64` directory):

```json
{
  "mcpServers": {
    "osca": {
      "command": "python3",
      "args": ["<OSCA_DIR>/osca-mcp/mcp_server.py"]
    }
  }
}
```

Restart your AI tool, then ask questions in natural language:

- "Create an ORM from my methylation data"
- "Run a mixed linear model association analysis with covariates"
- "What flags does OSCA support for eQTL analysis?"

### Available MCP Tools

| Tool | Description |
|------|-------------|
| `osca_info()` | Check OSCA binary status and version |
| `osca_help(topic)` | Get OSCA documentation (`overview`, `commands`, `flags`, `examples`, `formats`) |
| `run_osca(args, workdir)` | Execute any OSCA command; returns stdout, stderr, output files, and log |
| `list_files(path, pattern)` | List files in a directory |
| `read_file(path, max_lines)` | Read file contents with pagination |

See `osca-1.22-linux-x86_64/Readme.txt` for full configuration details.
