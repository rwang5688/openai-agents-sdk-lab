# Project Intake: OpenAI Agents Stack Learning Lab

## Purpose

This repository is a hands-on learning lab for the OpenAI Agents stack. The goal is to build a small, practical Streamlit application that demonstrates agent orchestration, specialist agents, tool use, observability, and production-minded design.

The project should stay compact and explainable. The best version of this lab is not the largest possible app; it is a clean multi-agent system that makes architectural tradeoffs visible and easy to reason about.

## Recommended Demo App

Build a "Research Assistant with Specialist Sub-Agents."

A user asks a business or technical question, such as:

```text
Should my company adopt OpenAI Agents SDK for customer support automation?
```

The application coordinates specialist agents:

- Research Agent: gathers useful technical and business context.
- Risk Agent: identifies implementation risks, operational concerns, security issues, and failure modes.
- Architecture Agent: proposes a practical implementation approach.
- Summary Agent: synthesizes the specialist outputs into an executive-ready recommendation.

The Streamlit UI should show:

- The user question.
- Specialist agent outputs.
- Final synthesized answer.
- Useful logs, traces, or execution metadata as the project matures.

## Suggested Stack

- Frontend: Streamlit.
- Agent framework: OpenAI Agents SDK.
- Environment management: `python-dotenv`.
- Optional persistence: SQLite.
- Optional observability: OpenAI tracing, structured logs, or OpenTelemetry.

Choose a current, cost-effective OpenAI model suitable for development. Keep the model choice easy to configure so the project can evolve.

## Minimal Architecture

```text
Streamlit UI
    |
Orchestrator
    |
--------------------------------
|              |               |
Research       Risk            Architecture
Agent          Agent           Agent
    \            |             /
     \           |            /
      -------- Summary Agent
```

The orchestrator should run independent specialist work in parallel where practical, combine the outputs, and ask the summary agent to produce the final response.

## Project Shape

A good starting structure:

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

This is a direction, not a hard requirement. Keep the structure proportional to the implementation.

## Engineering Priorities

- Build with small, readable modules.
- Use the OpenAI Agents SDK directly unless another dependency clearly earns its place.
- Keep agent roles focused and instructions concise.
- Prefer explicit orchestration over hidden framework magic.
- Isolate model/provider selection so future provider changes are easier.
- Add structured outputs when they make the UI or downstream evaluation more reliable.
- Include basic error handling from the beginning.
- Add retries, timeouts, logging, tracing, graceful degradation, and token budgeting as the app matures.
- Avoid excessive agents, heavy frontends, large vector database setup, or broad abstractions before they are needed.

## OpenAI and AWS Concept Mapping

The user is already familiar with AWS, Bedrock, Bedrock AgentCore, and Strands Agents. Use that background when framing OpenAI concepts:

- Strands Agents is a close conceptual parallel for OpenAI Agents SDK.
- Bedrock foundation models map conceptually to OpenAI models.
- Agent tool abstractions map to OpenAI function tools.
- Multi-agent collaboration maps to OpenAI handoffs and orchestration patterns.
- Agent tracing maps to OpenAI tracing and observability.
- MCP integrations are relevant in both ecosystems.

Step Functions can still be useful as a workflow-orchestration comparison, but it is more deterministic and state-machine driven. Strands Agents is usually the better conceptual comparison for LLM-directed, agent-centric orchestration.

## Learning Goals

Use this project to learn and demonstrate:

- Agent orchestration.
- Parallel specialist execution.
- Tool calling.
- Structured outputs.
- Observability and tracing.
- Clean separation between UI, orchestration, agents, tools, and providers.
- Production concerns such as partial failures, rate limits, prompt injection, hallucinations, messy input data, and source quality.

## High-Leverage Enhancements

Add one meaningful enhancement at a time:

1. Tracing or structured logging.
2. Tool calling for research or domain-specific lookups.
3. Retrieval over uploaded files.
4. Structured output schemas.
5. Evals and regression checks.
6. Guardrails or human approval workflows.
7. Streaming responses.

## Design Notes

Keep the demo simple, clean, and explainable. A useful project review should be able to cover:

- What problem the app solves.
- How the orchestrator and specialist agents work together.
- Why the work is split across agents.
- Why independent work can run in parallel.
- How the final synthesis improves the user experience.
- What can fail in production.
- What should be improved next.

## Things to Avoid

- Overly large orchestration frameworks before the project needs them.
- Too many agents.
- Unnecessary React or frontend complexity.
- Complex vector database setup before retrieval is actually needed.
- Line-by-line explanations as the main documentation style.
- Abstractions that obscure the learning value of the OpenAI Agents stack.
