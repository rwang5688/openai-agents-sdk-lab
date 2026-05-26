# TASKS

## 0. Stabilize Local Python

- [x] Confirm `python` resolves to `D:\Python313\python.exe` in PowerShell and Git Bash.
- [x] Bootstrap pip if needed:
  ```cmd
  D:\Python313\python.exe -m ensurepip --upgrade
  ```
- [x] Create a local virtual environment:
  ```cmd
  cd /d D:\workspace\openai-agents-sdk-lab
  D:\Python313\python.exe -m venv .venv
  .venv\Scripts\activate
  ```
- [x] Confirm the venv interpreter:
  ```cmd
  python --version
  where python
  ```

## 1. Project Skeleton

- [x] Create the first app structure:
  ```text
  streamlit_app/
    app.py
    research_assistant/
      __init__.py
      orchestrator.py
      specialists.py
      settings.py
      validation.py
    requirements.txt
    .env.example
    run.ps1
    run.sh
  ```
- [x] Add dependencies for Streamlit, OpenAI Agents SDK, dotenv loading, and test tooling.
- [x] Update `README.md` with setup, environment variables, and run instructions.

## 2. First Working Streamlit App

- [x] Build a compact Streamlit UI with:
  - Question input.
  - Run button.
  - Visible specialist outputs.
  - Final executive recommendation.
- [x] Add basic input validation for empty or overly long questions.
- [x] Show useful failure messages without exposing secrets or raw tracebacks.

## 3. Agent Definitions

- [x] Define concise specialist agent roles:
  - Research agent.
  - Risk analysis agent.
  - Architecture guidance agent.
  - Executive synthesis agent.
- [x] Keep instructions role-specific, evaluable, and easy to explain in a walkthrough.
- [x] Use explicit output contracts where helpful for rendering.

## 4. Orchestration Flow

- [x] Implement an orchestrator that accepts a user question.
- [x] Run independent specialist work in parallel where appropriate.
- [x] Collect partial results and pass them to the synthesis agent.
- [x] Return a structured result that the UI can render predictably.
- [x] Add graceful partial-failure behavior so one failed specialist does not destroy the whole run.

## 5. Provider and Configuration Boundary

- [x] Isolate model selection and OpenAI client configuration in `streamlit_app/research_assistant/settings.py`.
- [x] Load `OPENAI_API_KEY` from the environment.
- [x] Document required environment variables in `.env.example` and `README.md`.
- [x] Avoid committing secrets.
- [x] Add launch scripts that load `streamlit_app/.env.local` and run `streamlit_app/app.py`.

## 6. Production-Minded Baseline

- [x] Add simple structured logging around orchestration steps.
- [x] Add timeout handling for agent runs.
- [ ] Add lightweight token/input budgeting.
- [x] Capture enough metadata to explain what happened during a run.

## 7. Tests

- [x] Add focused tests for:
  - Orchestrator result shape.
  - Partial failure handling.
  - Empty input validation.
  - Specialist output formatting contracts.
- [x] Prefer mocks/fakes for model calls so tests run without an API key.

## 8. Demo Walkthrough

- [ ] Add a sample business or technical question to the README.
- [ ] Document the architecture in plain language.
- [ ] Explain why specialist separation helps.
- [ ] Explain why parallel execution is useful.
- [ ] Include production risks and next improvements:
  - Hallucinations.
  - Prompt injection.
  - Rate limits.
  - Poor source quality.
  - Evals.
  - Guardrails.
  - Retrieval grounding.
  - Human approval.

## 9. Follow-On Enhancements

- [ ] Add an IT knowledge base for Enterprise AI Adoption, Security & Governance, and Technical Strategy policies/guidance.
- [ ] Add OpenAI tracing or richer structured logs.
- [ ] Add one real tool for research or domain lookup.
- [ ] Add structured outputs for reliable UI rendering.
- [ ] Add uploaded document retrieval.
- [ ] Add evals and regression checks.
- [ ] Add guardrails or human approval for sensitive workflows.
