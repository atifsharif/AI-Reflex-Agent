# CRM Lead Qualifier — AI Reflex-Style Agent

A Python-based, LLM-powered **CRM Lead Qualifier Agent** that uses OpenAI tool calling to enrich sales leads, check CRM engagement history, calculate a priority score, and generate a concise summary for sales representatives.

> **Agent classification:** This is a *reflex-style, tool-calling agent*, not a strict simple reflex agent. It uses an LLM, conversation history, and conditional tool execution to decide what to do next.

## Features

- Extracts a company domain from a lead's email address.
- Retrieves mock company industry, size, and revenue information.
- Checks mock CRM history for prior engagement.
- Assigns a **High**, **Medium**, or **Low** lead score using deterministic Python rules.
- Produces a readable lead qualification summary with OpenAI.
- Keeps API credentials outside source control using a `.env` file.

## Project structure

```text
CRM_Lead_Agent/
├── main.py             # OpenAI client and agent execution loop
├── functions.py        # Domain lookup, CRM lookup, and scoring logic
├── tool_schema.py      # Tool definitions sent to the OpenAI model
├── config.py           # Environment variable loading
├── .env                # Local secrets (never commit)
├── .env.example        # Safe environment variable template
├── .gitignore          # Git exclusions
├── requirements.txt    # Python dependencies
└── README.md
```

## Architecture

```text
Lead email
   |
   v
main.py --> OpenAI model (tool schemas from tool_schema.py)
   |                  |
   |<-- tool calls ---|
   v
functions.py
   |-- lookup_domain_info(domain)
   |-- check_crm_history(email)
   `-- calculate_lead_score(data_summary)
   |
   v
Tool results appended to conversation history
   |
   v
OpenAI model --> Final lead summary
```

The model **requests** tools; the Python application **executes** them. The application then sends each result back to the model using the corresponding `tool_call_id`.

## Requirements

- Python 3.10 or newer
- An OpenAI API key with access to the configured model
- Internet access for OpenAI API requests

## Installation

1. Clone your repository and enter the project folder:

   ```bash
   git clone https://github.com/YOUR_USERNAME/CRM_Lead_Agent.git
   cd CRM_Lead_Agent
   ```

2. Create and activate a virtual environment:

   **Windows PowerShell**
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS / Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   The required packages are:

   ```text
   openai
   python-dotenv
   ```

4. Create `.env` in the project root (or copy `.env.example`) and set:

   ```dotenv
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   The `config.py` module should load it using `python-dotenv`:

   ```python
   import os
   from dotenv import load_dotenv

   load_dotenv()
   OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
   ```

## Run the agent

From the project root:

```bash
python main.py
```

Enter a lead email when prompted:

```text
Enter lead email: bob@widgetco.net
```

### Example execution

```text
--- Running Lead Qualifier Agent ---

[AI Thinking...]
-> TOOL ACTIVATED: Looking up widgetco.net
-> TOOL ACTIVATED: Checking CRM for bob@widgetco.net

[AI Thinking...]
-> TOOL ACTIVATED: Calculating lead score

[AI Thinking...]
--- FINAL AGENT SUMMARY ---
Lead: bob@widgetco.net
Company industry: Manufacturing
Company size: 100-250 employees
Estimated revenue: $10M - $25M
CRM status: Active Opportunity
Lead priority: High
```

*Illustrative output; the actual wording and tool-call sequence may vary.*

## Available tools

| Tool | Input | Output | Purpose |
|---|---|---|---|
| `lookup_domain_info` | `domain` | JSON string with industry, size, revenue | Enrich company data |
| `check_crm_history` | `email` | JSON string with last contact, status, notes | Check prior engagement |
| `calculate_lead_score` | `data_summary` | JSON string with lead score | Prioritize the lead |

### Scoring rules

Rules are evaluated in this order:

1. **High** if company revenue begins with `$1B+`.
2. **High** if CRM status is `Active Opportunity`.
3. **Medium** if company revenue begins with `$50M`.
4. **Low** otherwise.

These are **demonstration rules**, not validated predictive lead scores.

## How the agent works

1. `main.py` sends the user request and tool schemas to the OpenAI Chat Completions API.
2. The model can request one or more functions.
3. The agent maps requested function names to implementations in `AVAILABLE_FUNCTIONS`.
4. Python parses arguments and executes each function.
5. The returned JSON data is added to conversation history, with each result linked to its tool call.
6. After both enrichment lookups complete, the scoring tool receives the collected results.
7. The model generates a final summary. The loop stops when the model returns no further tool calls, or raises an error after the maximum iteration count.

**Note:** `tool_choice="auto"` means the model can choose not to call tools. The system prompt guides the desired sequence but does not guarantee it; production code should validate required steps before accepting a final answer.

## API key and GitHub security

Never hardcode your OpenAI API key in Python source files or commit `.env`.

Recommended `.gitignore`:

```gitignore
.env
.env.*
!.env.example
.venv/
venv/
__pycache__/
*.pyc
```

Before committing, check that `.env` is ignored:

```bash
git check-ignore -v .env
git status
```

If a real API key has already been committed or published, **revoke/rotate it immediately**. Adding `.env` to `.gitignore` does not remove secrets from existing Git history.

### Publish to GitHub

After creating an empty repository on GitHub:

```bash
git init
git branch -M main
git add .
git diff --cached --name-only
git commit -m "Initial CRM lead agent"
git remote add origin https://github.com/YOUR_USERNAME/CRM_Lead_Agent.git
git push -u origin main
```

Verify the staged file list contains no secrets before committing.

## Current limitations

- Company and CRM data are **hardcoded mock records**; no real enrichment or CRM service is connected.
- The lead scoring algorithm is rule-based, not a trained machine learning model.
- The email check is minimal and not full address validation.
- Agent state is kept in memory for one run and is not saved to a database.
- Tool use and final-answer completion depend partly on model behavior.
- OpenAI API requests may incur usage charges.

## Potential improvements

- Connect real CRM APIs such as Salesforce or HubSpot.
- Replace mock company data with a real enrichment service.
- Add unit tests for each scoring rule and error case.
- Add structured logging, retries, and stronger input validation.
- Store lead history and scores in a database.
- Enforce required tool completion before allowing a final answer.
- Add a REST API or web interface.

## Disclaimer

This project is intended for learning and demonstration. The company data, CRM history, and scoring rules are illustrative and should not be treated as verified business intelligence.
