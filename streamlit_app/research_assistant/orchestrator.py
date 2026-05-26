import asyncio
import logging
import time
from dataclasses import dataclass

from agents import Runner, trace

from .specialists import (
    build_architecture_agent,
    build_research_agent,
    build_risk_agent,
    build_summary_agent,
)


SPECIALIST_TIMEOUT_SECONDS = 90
logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TokenUsage:
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    requests: int = 0


@dataclass(frozen=True)
class SpecialistResult:
    name: str
    output: str
    error: str | None = None
    elapsed_seconds: float = 0.0
    token_usage: TokenUsage = TokenUsage()


@dataclass(frozen=True)
class TraceEvent:
    step: str
    agent: str
    status: str
    elapsed_seconds: float
    token_usage: TokenUsage = TokenUsage()
    detail: str = ""


@dataclass(frozen=True)
class WorkflowResult:
    final_recommendation: str
    specialist_results: list[SpecialistResult]
    trace_events: list[TraceEvent]
    trace_id: str
    metadata: dict[str, str | int | float]


async def _run_specialist(agent_name: str, agent, question: str) -> SpecialistResult:
    started = time.perf_counter()
    prompt = (
        f"Question:\n{question}\n\n"
        "Return a concise markdown analysis with headings and bullets."
    )
    try:
        logger.info("specialist_started", extra={"specialist": agent_name})
        result = await asyncio.wait_for(
            Runner.run(agent, prompt),
            timeout=SPECIALIST_TIMEOUT_SECONDS,
        )
    except Exception as exc:
        elapsed = round(time.perf_counter() - started, 2)
        logger.warning(
            "specialist_failed",
            extra={"specialist": agent_name, "error": str(exc)},
        )
        return SpecialistResult(
            name=agent_name,
            output="",
            error=f"{agent_name} failed: {exc}",
            elapsed_seconds=elapsed,
        )

    elapsed = round(time.perf_counter() - started, 2)
    logger.info("specialist_completed", extra={"specialist": agent_name})
    return SpecialistResult(
        name=agent_name,
        output=result.final_output,
        elapsed_seconds=elapsed,
        token_usage=_extract_token_usage(result),
    )


async def run_research_workflow(question: str, model: str) -> WorkflowResult:
    started = time.perf_counter()
    logger.info("workflow_started", extra={"model": model})

    with trace(
        "Research Assistant Workflow",
        metadata={"model": model, "app": "openai-agents-sdk-lab"},
    ) as current_trace:
        specialists = [
            ("Research", build_research_agent(model)),
            ("Risk Analysis", build_risk_agent(model)),
            ("Architecture Guidance", build_architecture_agent(model)),
        ]

        specialist_results = await asyncio.gather(
            *[
                _run_specialist(name, agent, question)
                for name, agent in specialists
            ]
        )

        synthesis_prompt = _build_synthesis_prompt(question, specialist_results)
        synthesis_started = time.perf_counter()
        summary_result = await Runner.run(build_summary_agent(model), synthesis_prompt)
        synthesis_elapsed = round(time.perf_counter() - synthesis_started, 2)
        synthesis_usage = _extract_token_usage(summary_result)

        trace_id = current_trace.trace_id

    elapsed = round(time.perf_counter() - started, 2)
    failed_count = sum(1 for result in specialist_results if result.error)
    trace_events = [
        TraceEvent(
            step="specialist",
            agent=result.name,
            status="failed" if result.error else "completed",
            elapsed_seconds=result.elapsed_seconds,
            token_usage=result.token_usage,
            detail=result.error or "Generated specialist analysis.",
        )
        for result in specialist_results
    ]
    trace_events.append(
        TraceEvent(
            step="synthesis",
            agent="Executive Synthesis",
            status="completed",
            elapsed_seconds=synthesis_elapsed,
            token_usage=synthesis_usage,
            detail="Generated executive recommendation.",
        )
    )
    total_usage = _sum_token_usage(
        [result.token_usage for result in specialist_results] + [synthesis_usage]
    )

    logger.info(
        "workflow_completed",
        extra={"elapsed_seconds": elapsed, "failed_specialist_count": failed_count},
    )

    return WorkflowResult(
        final_recommendation=summary_result.final_output,
        specialist_results=list(specialist_results),
        trace_events=trace_events,
        trace_id=trace_id,
        metadata={
            "specialist_count": len(specialist_results),
            "failed_specialist_count": failed_count,
            "elapsed_seconds": elapsed,
            "model": model,
            "input_tokens": total_usage.input_tokens,
            "output_tokens": total_usage.output_tokens,
            "total_tokens": total_usage.total_tokens,
            "requests": total_usage.requests,
        },
    )


def _extract_token_usage(result) -> TokenUsage:
    usage_items = []

    context_usage = getattr(getattr(result, "context_wrapper", None), "usage", None)
    if context_usage is not None:
        usage_items.append(context_usage)

    for response in getattr(result, "raw_responses", []) or []:
        response_usage = getattr(response, "usage", None)
        if response_usage is not None:
            usage_items.append(response_usage)

    if not usage_items:
        return TokenUsage()

    # Prefer request_usage_entries when present to avoid double-counting aggregate
    # context usage plus raw response usage for the same model call.
    request_entries = []
    for usage in usage_items:
        request_entries.extend(getattr(usage, "request_usage_entries", []) or [])

    if request_entries:
        return _sum_token_usage([_usage_from_object(entry) for entry in request_entries])

    return _sum_token_usage([_usage_from_object(usage) for usage in usage_items])


def _usage_from_object(usage) -> TokenUsage:
    return TokenUsage(
        input_tokens=int(getattr(usage, "input_tokens", 0) or 0),
        output_tokens=int(getattr(usage, "output_tokens", 0) or 0),
        total_tokens=int(getattr(usage, "total_tokens", 0) or 0),
        requests=int(getattr(usage, "requests", 1) or 1),
    )


def _sum_token_usage(usages: list[TokenUsage]) -> TokenUsage:
    return TokenUsage(
        input_tokens=sum(usage.input_tokens for usage in usages),
        output_tokens=sum(usage.output_tokens for usage in usages),
        total_tokens=sum(usage.total_tokens for usage in usages),
        requests=sum(usage.requests for usage in usages),
    )


def _build_synthesis_prompt(
    question: str,
    specialist_results: list[SpecialistResult],
) -> str:
    sections = []
    for result in specialist_results:
        if result.error:
            content = f"Unavailable. Error: {result.error}"
        else:
            content = result.output
        sections.append(f"## {result.name}\n{content}")

    return (
        f"Original question:\n{question}\n\n"
        "Specialist analysis:\n\n"
        + "\n\n".join(sections)
        + "\n\nCreate a concise executive recommendation with: "
        "recommendation, rationale, risks, mitigations, and next steps."
    )
