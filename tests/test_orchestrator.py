import asyncio
from types import SimpleNamespace

from streamlit_app.research_assistant import orchestrator


def fake_result(output, input_tokens=10, output_tokens=5):
    total_tokens = input_tokens + output_tokens
    usage = SimpleNamespace(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        request_usage_entries=[],
        requests=1,
    )
    return SimpleNamespace(
        final_output=output,
        raw_responses=[SimpleNamespace(usage=usage)],
        context_wrapper=None,
    )


def test_run_research_workflow_returns_expected_shape(monkeypatch):
    async def fake_run(agent, prompt):
        if agent.name == "Executive Synthesis Specialist":
            return fake_result("Final recommendation", input_tokens=20, output_tokens=10)
        return fake_result(f"{agent.name} output")

    monkeypatch.setattr(orchestrator.Runner, "run", fake_run)

    result = asyncio.run(
        orchestrator.run_research_workflow("Should we adopt this?", model="test-model")
    )

    assert result.final_recommendation == "Final recommendation"
    assert len(result.specialist_results) == 3
    assert result.metadata["specialist_count"] == 3
    assert result.metadata["failed_specialist_count"] == 0
    assert result.metadata["model"] == "test-model"
    assert result.metadata["input_tokens"] == 50
    assert result.metadata["output_tokens"] == 25
    assert result.metadata["total_tokens"] == 75
    assert result.metadata["requests"] == 4
    assert result.trace_id.startswith("trace_")
    assert [event.agent for event in result.trace_events] == [
        "Research",
        "Risk Analysis",
        "Architecture Guidance",
        "Executive Synthesis",
    ]


def test_run_research_workflow_preserves_partial_failures(monkeypatch):
    async def fake_run(agent, prompt):
        if agent.name == "Risk Specialist":
            raise RuntimeError("risk unavailable")
        if agent.name == "Executive Synthesis Specialist":
            assert "Risk Analysis failed: risk unavailable" in prompt
            return fake_result("Final with caveat")
        return fake_result(f"{agent.name} output")

    monkeypatch.setattr(orchestrator.Runner, "run", fake_run)

    result = asyncio.run(
        orchestrator.run_research_workflow("What can go wrong?", model="test-model")
    )

    assert result.final_recommendation == "Final with caveat"
    assert result.metadata["failed_specialist_count"] == 1
    assert any(
        item.name == "Risk Analysis" and item.error
        for item in result.specialist_results
    )
    assert any(
        event.agent == "Risk Analysis" and event.status == "failed"
        for event in result.trace_events
    )
