# subagent
![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![uv](https://img.shields.io/badge/package_manager-uv-orange.svg)

A command-line AI coding agent built in Python using Google's Gemini API. It explores codebases, reads and writes files, executes scripts, and iterates in a feedback loop until it completes a task.

---

## What it does

You pass a prompt on the command line. The agent sends it to Gemini along with a set of available tools, then enters a loop: the model decides which tool to call, the program executes it and feeds the result back, and this repeats until the model produces a final text answer. Full conversation history is maintained across iterations so the model has complete context at every step.

```bash
uv run main.py "Read calculator/main.py and tell me what it does"
```

## Agent loop

```text
User prompt
     │
     ▼
┌─────────────┐       tool call        ┌───────────────┐
│  Gemini API │ ─────────────────────► │ call_function │
│  (model)    │ ◄───────────────────── │ (dispatcher)  │
└─────────────┘       tool result      └───────────────┘
     │
     │ final text answer (no more tool calls)
     ▼
  Output to user
```

The loop is capped at a configurable max iteration count (`MAX_ITERS` in `config.py`) to prevent runaway agents.

## Tools

All file tools are restricted to a sandboxed working directory. Scripts run via run_python_file are not isolated and execute with your user's permissions. Every path is validated against the resolved working directory before any filesystem operation runs.

| Tool | Description |
|------|-------------|
| `get_files_info` | List directory contents and file sizes |
| `get_file_content` | Read a file's contents (with a size limit) |
| `write_file` | Write or overwrite a file, creating nested directories as needed |
| `run_python_file` | Execute a Python file using the current interpreter (`sys.executable`) |

## Architecture notes

**Central dispatcher (`call_function`)** routes the model's tool requests to the right Python function via a module-level `function_map`. It injects the working directory path into every tool call, so the model never has to (or is able to) specify an absolute path, and prevents path traversal outside the sandbox.

**Sandboxing** is enforced with `os.path.commonpath`, comparing the resolved absolute target path against the resolved absolute working directory. Any path that escapes the working directory (`../`, `/bin`, `/tmp`, etc.) is rejected before any file operation is attempted.

## Setup

**Prerequisites:** Python 3.13+, [uv](https://github.com/astral-sh/uv)

**1. Clone the repo and install dependencies**

```bash
git clone https://github.com/amelfia/subagent.git
cd subagent
uv sync
```

**2. Create a `.env` file in the project root**

```text
GEMINI_API_KEY=your_key_here
```

Get a free API key from [Google AI Studio](https://aistudio.google.com/apikey).

**3. Run it**

```bash
uv run main.py "your prompt here"
```

## Example

```bash
uv run main.py "Look at the calculator app and fix any bugs you find"
```

The agent will explore the `calculator/` directory, read the source files, identify issues, and write fixes, all autonomously.

## Tech stack

- **Python:** core language
- **Google Gemini API (`google-genai`):** the underlying model
- **uv:** dependency and environment management
- **python-dotenv:** API key loading from `.env`

## Project structure

```text
subagent/
├── main.py                     # Entry point; parses CLI args and starts the agent loop
├── config.py                   # Model config and agent settings (e.g. max iterations)
├── prompts.py                  # System prompt definition
├── functions/
│   ├── call_function.py        # Central dispatcher; routes tool calls and injects deps
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   └── run_python_file.py
├── calculator/                 # Sample codebase for the agent to operate on
│   ├── main.py
│   ├── tests.py
│   └── pkg/
│       ├── calculator.py
│       └── render.py
├── tests/                      # Manual verification scripts for each tool
│   ├── test_get_file_content.py
│   ├── test_get_files_info.py
│   ├── test_run_python_file.py
│   └── test_write_file.py
├── pyproject.toml
├── requirements.txt
└── .gitignore
```

## Gitignored files

- `.env`: contains your API key
- `__pycache__/`, `.venv/`: standard Python/venv artifacts
