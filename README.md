# openai-agents-sdk-lab

A small learning lab for building a Streamlit research assistant with the OpenAI Agents SDK.

The app will take a business or technical question, run specialist agents for research, risk, and architecture guidance, then synthesize an executive-ready recommendation.

## Setup

Create and activate a virtual environment:

```cmd
cd /d D:\workspace\openai-agents-sdk-lab
D:\Python313\python.exe -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```cmd
python -m pip install -r streamlit_app\requirements.txt
```

Create `streamlit_app\.env.local` from `streamlit_app\.env.example` and set:

```text
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-5.4-mini
```

Run the app directly:

```cmd
python -m streamlit run streamlit_app/app.py
```

Or use a launcher script that loads `.env.local` first:

```powershell
.\streamlit_app\run.ps1
```

```bash
./streamlit_app/run.sh
```

## Architecture

```text
streamlit_app/
  .env.example
  app.py
  requirements.txt
  research_assistant/
    orchestrator.py
    settings.py
    specialists.py
    validation.py
  run.ps1
  run.sh
```

The internal package is named `research_assistant` instead of `agents` because the OpenAI Agents SDK imports from the package name `agents`.

## Current Demo Goal

Build a compact, explainable multi-agent workflow:

- Research specialist identifies relevant facts, assumptions, and unknowns.
- Risk specialist reviews operational, security, compliance, reliability, cost, and adoption risks.
- Architecture specialist explains integration choices and enterprise tradeoffs.
- Executive synthesis specialist turns the specialist outputs into a recommendation.
