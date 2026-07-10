Usage

1.Run the executable:
./osca


Documentation

For detailed instructions on how to use OSCA, please refer to the official website: https://yanglab.westlake.edu.cn/software/osca/#Overview


================================================================================
MCP Server - Talk to OSCA via AI Tools (Claude / Codex / opencode)
================================================================================

This directory includes an MCP (Model Context Protocol) server that lets you
use OSCA through natural-language conversation with AI assistants.

--------------------------------------------------------------------------------
1. PREREQUISITES
--------------------------------------------------------------------------------

- Python 3.10+
- Install the MCP SDK:

    pip install mcp

--------------------------------------------------------------------------------
2. CONFIGURE YOUR AI TOOL
--------------------------------------------------------------------------------

Replace <OSCA_DIR> below with the real path to this
directory (the folder containing the osca binary).

--- Claude Desktop ---
Edit ~/Library/Application Support/Claude/claude_desktop_config.json:

    {
      "mcpServers": {
        "osca": {
          "command": "python3",
          "args": ["<OSCA_DIR>/osca-mcp/mcp_server.py"]
        }
      }
    }

--- opencode ---
Edit .opencode.json (project-level) or ~/.config/opencode/opencode.json:

    {
      "mcpServers": {
        "osca": {
          "type": "local",
          "command": ["python3", "<OSCA_DIR>/osca-mcp/mcp_server.py"]
        }
      }
    }

--- Codex (OpenAI) ---
Edit ~/.codex/config.json:

    {
      "mcpServers": {
        "osca": {
          "command": "python3",
          "args": ["<OSCA_DIR>/osca-mcp/mcp_server.py"]
        }
      }
    }

--------------------------------------------------------------------------------
3. AVAILABLE MCP TOOLS
--------------------------------------------------------------------------------

  osca_info()                 Check OSCA binary status & version
  osca_help(topic)            Get OSCA docs
                              topics: overview, commands, flags, examples, formats
  run_osca(args, workdir)     Run any OSCA command, returns stdout/stderr/files/log
  list_files(path, pattern)   List files in a directory
  read_file(path, max_lines)  Read file contents with pagination

--------------------------------------------------------------------------------
4. EXAMPLE CONVERSATIONS
--------------------------------------------------------------------------------

You: "Create an ORM from my methylation data in meth.eFile"
AI:  calls run_osca(["--efile", "meth", "--methylation", "--make-orm", "--out", "meth_orm"])

You: "Run a linear regression association analysis"
AI:  calls run_osca(["--efile", "data", "--linear", "--pheno", "pheno.txt", "--out", "result"])

You: "What commands does OSCA support?"
AI:  calls osca_help("commands") then summarizes for you
