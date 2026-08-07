---
type: concept
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/concept
  - protocol
  - architecture
  - tooling
confidence: high
source_count: 1
---

# FastMCP Protocol

Model Context Protocol (FastMCP) v2 is a standard for LLMs to use external tools. Tools are separate programs that implement a tool interface; the LLM can invoke them dynamically. [[brAIniac]] uses FastMCP to integrate time, search, and future tools without modifying core chat logic.

## Definition

**FastMCP (Model Context Protocol) v2:**
- Standard protocol for LLMs to discover and call tools
- Tools are separate microservices (not embedded in LLM)
- LLM describes what it needs; tool provider implements it
- Designed for local, safe, controlled tool execution

**Key Innovation:** Decouple LLM from tools. Same LLM can use different tools in different contexts.

## Problem It Solves

**Before MCP (Function Calling):**
```python
# Tightly coupled - tools hardcoded in LLM interface
if user_query.contains("time"):
    result = get_current_time()
elif user_query.contains("search"):
    result = web_search(query)
else:
    result = llm.generate(query)
```

**Issues:**
- ❌ LLM doesn't know what tools exist
- ❌ Can't add new tools without modifying LLM
- ❌ Difficult to version tools independently
- ❌ Security: LLM has direct access to all functions

**With MCP (Decoupled):**
```python
# MCP discovers tools dynamically
available_tools = mcp_server.list_tools()
# LLM chooses which tools to call
response = llm.generate(query, available_tools)
# Tool call routed to appropriate tool server
result = mcp.call_tool(tool_name, arguments)
```

**Advantages:**
- ✅ LLM discovers tools at runtime
- ✅ Add new tools without restarting LLM
- ✅ Multiple tool servers can coexist
- ✅ Security: LLM can't do anything not explicitly in tools
- ✅ Tools are versionable independently

## Architecture

### Tool Server Pattern

```
Tool Server (separate process)
├─ Tool 1: current_time()
├─ Tool 2: web_search(query)
└─ Tool 3: file_search(pattern)
    ↓ (implements MCP interface)
Expose via:
├─ STDIO (same machine, fast)
├─ HTTP (different machine, scalable)
└─ WebSocket (streaming results)
```

### Full Flow

```
User: "What time is it?"
    ↓
brAIniac ChatEngine
├─ Sends query to Ollama LLM
├─ Includes available_tools from MCP
└─ Passes tool schema to LLM
    ↓
Ollama (with tool awareness)
├─ Recognizes query needs tool
└─ Outputs: {"tool": "current_time", "args": {}}
    ↓
ChatEngine
├─ Routes to tool server
└─ Sends: (tool_name="current_time", args={})
    ↓
MCP Tool Server
├─ Executes current_time()
└─ Returns: "2024-12-07 14:30:45 UTC"
    ↓
ChatEngine
├─ Receives result
├─ Sends result back to LLM: "current time is 14:30:45"
└─ LLM generates response
    ↓
Response to user: "It's currently 2:30 PM UTC."
```

## MCP v2 Standards (How brAIniac Implements)

### Tool Schema

Every tool must describe itself:

```python
from fastmcp import FastMCP

app = FastMCP("brainiac-time-tools")

@app.tool()
def current_time():
    """
    Get the current time.
    
    Returns:
        str: Current time in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
    
    Example:
        >>> current_time()
        "2024-12-07T14:30:45Z"
    """
    from datetime import datetime
    return datetime.utcnow().isoformat() + "Z"
```

**Tool Schema (auto-generated from docstring):**
```json
{
  "name": "current_time",
  "description": "Get the current time.",
  "inputSchema": {
    "type": "object",
    "properties": {}
  },
  "returns": {
    "type": "string",
    "description": "Current time in ISO 8601 format"
  }
}
```

### Tool with Arguments

```python
@app.tool()
def web_search(query: str, max_results: int = 5) -> str:
    """
    Search the web using DuckDuckGo.
    
    Args:
        query: Search query string
        max_results: Maximum results to return (default 5)
    
    Returns:
        str: Formatted search results
    
    Example:
        >>> web_search("TTRPG news 2024", max_results=3)
        "1. Article Title - https://..."
    """
    import duckduckgo  # Local web search
    results = duckduckgo.search(query, max_results=max_results)
    formatted = "\n".join([f"{i+1}. {r['title']} - {r['url']}" 
                           for i, r in enumerate(results)])
    return formatted
```

**Auto-Generated Schema:**
```json
{
  "name": "web_search",
  "description": "Search the web using DuckDuckGo.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Search query string"
      },
      "max_results": {
        "type": "integer",
        "description": "Maximum results to return (default 5)"
      }
    },
    "required": ["query"]
  }
}
```

### LLM Tool Use Format

When LLM wants to use a tool, it outputs:

```json
{
  "tool_calls": [
    {
      "id": "call_123",
      "function": {
        "name": "web_search",
        "arguments": "{\"query\": \"TTRPG D&D news\"}"
      }
    }
  ]
}
```

ChatEngine receives this and:
```python
# 1. Parse tool call
tool_name = "web_search"
tool_args = {"query": "TTRPG D&D news"}

# 2. Route to tool server
tool_result = mcp.call_tool(tool_name, **tool_args)

# 3. Send result back to LLM for synthesis
llm_response = llm.generate(
    previous_response + tool_result,
    available_tools
)
```

## Using MCP in brAIniac

### Current Tools (Phase 1)

**Available tools in brAIniac:**

1. **current_time()**
   - Returns current time
   - No arguments
   - Use case: Check timestamp

2. **web_search(query, max_results=5)**
   - Search DuckDuckGo
   - Optional max_results
   - Use case: Look up current info

### Adding New Tools (Phase 2+)

**To add a new tool, create a tool server:**

```python
# servers/ttrpg_tools/server.py
from fastmcp import FastMCP
import random

app = FastMCP("brainiac-ttrpg-tools")

@app.tool()
def roll_dice(num_dice: int = 1, num_sides: int = 20) -> str:
    """
    Roll D&D-style dice.
    
    Args:
        num_dice: Number of dice to roll (default 1)
        num_sides: Sides per die (default 20)
    
    Returns:
        str: Roll results and total
    
    Example:
        >>> roll_dice(3, 6)
        "Rolled 3d6: [4, 5, 2] = 11"
    """
    rolls = [random.randint(1, num_sides) for _ in range(num_dice)]
    total = sum(rolls)
    return f"Rolled {num_dice}d{num_sides}: {rolls} = {total}"
```

**Register in brAIniac:**

```python
# core/chat.py
from servers.ttrpg_tools.server import app as ttrpg_tools

self.available_tools = [
    self.time_tools.list_tools(),
    self.search_tools.list_tools(),
    ttrpg_tools.list_tools(),  # New tools available
]
```

**Now LLM can use:**
```
User: "Roll for initiative!"
LLM: "I'll roll for you!"
→ Calls: roll_dice(1, 20)
→ Returns: "Rolled 1d20: [16] = 16"
Response: "You rolled a 16 for initiative!"
```

## Comparison: Function Calling vs. MCP

| Aspect | Function Calling | MCP |
|--------|------------------|-----|
| **Coupling** | Tight (in LLM code) | Loose (separate servers) |
| **Tool Discovery** | Predefined | Dynamic (MCP registry) |
| **Versioning** | LLM + tools together | Independent versions |
| **Scalability** | Single LLM → limited tools | Multiple tool servers |
| **Security** | LLM has direct access | Explicit tool permissions |
| **Local/Cloud** | Either | Both (STDIO, HTTP, WebSocket) |
| **Standard** | OpenAI specific | Anthropic standard (open) |

## MCP Use Cases in Your Ecosystem

### brAIniac (Phase 1)
```
Tools:
- current_time() [local]
- web_search() [local with DuckDuckGo]
```

### brAIniac (Phase 2 Planned)
```
Additional tools:
- research_server (IterDRAG + SearXNG)
- local_file_search (find docs)
- execute_code_sandbox (run Python safely)
- knowledge_cache (CAG-based lookup)
```

### Integration Opportunity
```
Could add:
- GenerateIdeas as tool
  "Give me a programming idea"
  → brAIniac calls GenerateIdeas tool
  
- TTRPG lookup as tool
  "What are the fireball spell rules?"
  → brAIniac calls TTRPG-RAG tool
  → Return results
```

## Security Considerations

**MCP provides safety because:**

1. **Explicit Tool List**
   - LLM can only see tools you expose
   - Can't access filesystem unless you give file_read tool

2. **Argument Validation**
   - Tool schema validates inputs
   - Can't pass unexpected arguments

3. **Execution Sandbox**
   - Tools run in separate process
   - Can monitor/limit resources

4. **Permissions**
   - Each tool can require permission
   - Example: file deletion needs explicit approval

**Example: Safe file access**
```python
@app.tool()
def read_document(file_path: str) -> str:
    """
    Read a document (ONLY from ~/documents directory).
    
    Args:
        file_path: Filename (must be in ~/documents)
    
    Returns:
        str: File contents
    """
    import os
    from pathlib import Path
    
    # Security: Only allow ~/documents
    allowed_dir = Path.home() / "documents"
    requested = Path(file_path).resolve()
    
    if not str(requested).startswith(str(allowed_dir)):
        return "ERROR: Only ~/documents allowed"
    
    return open(requested).read()
```

LLM can call `read_document("notes.txt")` but NOT `read_document("/etc/passwd")`

## MCP Ecosystem Standards

**Standardized tool categories:**

1. **System Tools**
   - Time, date, timezone
   - Environment variables
   - System info

2. **I/O Tools**
   - File read/write
   - Directory listing
   - File search

3. **Web Tools**
   - Web search
   - HTTP requests
   - RSS feeds

4. **Code Tools**
   - Execute code (sandboxed)
   - Syntax check
   - Format code

5. **Domain Tools**
   - TTRPG rules lookup
   - Medical queries
   - Legal research

## Related Concepts

- [[brAIniac]] — Uses FastMCP for tools
- [[AI/LLM Ecosystem]] — Tool coordination in your projects
- [[Local-First AI Architecture]] — MCP enables local tools

## Open Questions

- [How to handle tool timeouts in brAIniac?]
- [Should GenerateIdeas be a tool or separate?]
- [Tool permissions framework?]
- [Monitor tool usage for debugging?]
- [Rate limiting tools (prevent abuse)?]

## Resources

- Official MCP Documentation: https://modelcontextprotocol.io/
- FastMCP GitHub: https://github.com/jlouis/fastmcp
- Example Tool Servers: https://github.com/anthropics/mcp/examples

## Implementation in brAIniac

**Key files:**
- `servers/base_tools/server.py` — Current tools (time, search)
- `core/chat.py` — ChatEngine (tool coordination)
- `core/intent_classifier.py` — Decide when to use tools

**How to extend:**
1. Create new tool file in `servers/[category]/server.py`
2. Implement MCP tools with docstrings
3. Register in ChatEngine
4. LLM can now call tools

## Sources

- [[Wiki/entities/brAIniac]]
- MCP v2 Specification
- OpenAI Function Calling documentation
- Anthropic tool_use documentation
