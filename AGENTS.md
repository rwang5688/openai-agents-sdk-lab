# Project Guidance

## Project Intake

This repository is a learning lab for building with the OpenAI Agents stack. The target artifact is a small but polished Streamlit application that demonstrates a multi-agent system with clear orchestration, specialist agents, production-minded engineering, and an explainable architecture.

The intended demo direction is a "Research Assistant with Specialist Sub-Agents." A user asks a business or technical question, and the system runs specialist agents for research, risk analysis, and architecture guidance before synthesizing an executive-ready recommendation.

The project should favor a compact, credible build over a large or flashy one. The goal is to learn the OpenAI Agents stack by building something practical, explainable, and production-minded.

## Desired Architecture

Start with a simple, inspectable architecture:

- Streamlit UI for entering a question and viewing agent outputs.
- Orchestrator flow that coordinates specialist agents.
- Specialist agents for research, risk, architecture, and summary synthesis.
- Parallel execution where agent tasks are independent.
- A final synthesis step that produces an executive-facing recommendation.

Prefer a structure that can grow without becoming framework-heavy:

```text
app.py
agents/
  orchestrator.py
  specialists.py
tools/
  ...
providers/
  ...
requirements.txt
README.md
```

This layout is a target direction, not a rigid requirement. Keep the implementation proportional to the current scope.

## Engineering Priorities

- Build for clarity first: small modules, explicit boundaries, and readable control flow.
- Use the OpenAI Agents SDK directly unless there is a strong reason to add another orchestration framework.
- Keep the orchestration layer isolated enough that model/provider choices can evolve later.
- Make agent instructions concise, role-specific, and easy to evaluate.
- Prefer structured outputs when they improve reliability or make the UI easier to render.
- Add production considerations as the app matures: retries, timeout handling, graceful degradation, logging, tracing, input validation, token budgeting, and partial-failure behavior.
- Avoid over-engineering: no giant abstractions, excessive agent counts, complicated frontends, or large vector database setup unless the project explicitly grows in that direction.

## OpenAI and AWS Framing

The user's background is strong in AWS, Bedrock, Bedrock AgentCore, and Strands Agents. When explaining architecture or tradeoffs, map OpenAI concepts to that background thoughtfully:

- OpenAI Agents SDK is closest to Strands-style agent orchestration.
- OpenAI function tools map to agent/tool abstractions in AWS-oriented systems.
- OpenAI tracing and observability map conceptually to agent tracing and operational telemetry.
- Deterministic workflow engines such as Step Functions are useful comparison points, but they are not the best parallel for LLM-directed agent orchestration.

Where possible, design with enterprise portability in mind: reusable tools, isolated provider/model selection, and contracts that are not unnecessarily tied to one implementation detail.

## Demo and Learning Goals

The eventual walkthrough should feel like a clear architecture review:

- State the problem being solved.
- Show the architecture and agent responsibilities.
- Explain why multi-agent separation helps.
- Explain why independent work can run in parallel.
- Explain why a synthesis step improves user experience.
- Discuss failure modes such as hallucinations, messy customer data, prompt injection, partial failures, rate limits, and poor source quality.
- Describe next improvements such as evals, guardrails, retrieval grounding, human approval, persistent memory, and richer tracing.

Do not over-focus the walkthrough on line-by-line code. Emphasize decisions, tradeoffs, and operational readiness.

## Feature Roadmap

A strong first version should include:

- Working Streamlit UI.
- OpenAI Agents SDK integration.
- Specialist agents with visible intermediate outputs.
- Final executive summary output.
- Basic error handling and useful user-facing failure messages.

Good follow-on enhancements, in priority order:

1. Tracing or structured logging for observability.
2. Tool calling for research or domain-specific lookups.
3. Structured outputs for more reliable rendering and evaluation.
4. Retrieval over uploaded documents.
5. Evals and regression checks.
6. Guardrails or human approval for sensitive actions.

Choose one meaningful enhancement at a time. Simple, clean, and explainable is the preferred direction.

## Local Development Notes

- Keep setup instructions current in `README.md`.
- Do not commit secrets. Use `.env` for local API keys and document required environment variables.
- Prefer `requirements.txt` or another simple dependency manifest until the project needs more packaging structure.
- If adding a dev server or Streamlit app, verify it runs locally before handing work back.
- When adding tests, keep them focused on orchestration behavior, formatting contracts, and failure handling.

## Working Style for Codex

- Read existing files before changing structure.
- Make small, coherent edits that advance the learning project.
- Preserve the Kiro intake in `.kiro/steering/project-intake.md`; use this `AGENTS.md` as the Codex-facing working guide.
- Keep the user looped in on architectural choices and explain tradeoffs in terms useful for future project notes or demos.
- Prefer implementation over long proposals once the direction is clear.
