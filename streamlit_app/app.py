import asyncio

import streamlit as st

from research_assistant.runtime import configure_ssl_trust_store
from research_assistant.orchestrator import run_research_workflow
from research_assistant.sample_prompts import SAMPLE_PROMPTS
from research_assistant.settings import (
    get_default_model,
    get_supported_models,
    has_openai_api_key,
    load_environment,
)
from research_assistant.validation import validate_question


configure_ssl_trust_store()
load_environment()


st.set_page_config(
    page_title="Research Assistant",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        max-width: 1180px;
    }
    div[data-testid="stSidebar"] {
        border-right: 1px solid #e5e7eb;
    }
    div[data-testid="stSidebar"] h2,
    div[data-testid="stSidebar"] h3 {
        margin-top: 0.25rem;
    }
    .app-subtitle {
        color: #4b5563;
        margin-top: -0.5rem;
        max-width: 780px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "selected_model" not in st.session_state:
    st.session_state.selected_model = get_default_model()

if "question" not in st.session_state:
    st.session_state.question = ""

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "last_question" not in st.session_state:
    st.session_state.last_question = ""


def use_sample_prompt(prompt: str) -> None:
    st.session_state.question = prompt
    st.session_state.last_result = None
    st.session_state.last_question = ""


def clear_question() -> None:
    st.session_state.question = ""
    st.session_state.last_result = None
    st.session_state.last_question = ""


with st.sidebar:
    st.header("Run Settings")
    models = get_supported_models()
    selected_index = (
        models.index(st.session_state.selected_model)
        if st.session_state.selected_model in models
        else 0
    )
    st.session_state.selected_model = st.selectbox(
        "Model",
        models,
        index=selected_index,
        help="Applies to all specialist agents and the final synthesis step for this run.",
    )
    st.caption(f"Active model: `{st.session_state.selected_model}`")

    st.divider()
    st.subheader("Sample Prompts")
    for category, prompts in SAMPLE_PROMPTS.items():
        st.markdown(f"**{category}**")
        for label, prompt in prompts:
            st.button(
                label,
                key=f"sample-{category}-{label}",
                use_container_width=True,
                on_click=use_sample_prompt,
                args=(prompt,),
            )

st.title("Research Assistant")
st.markdown(
    "<p class='app-subtitle'>Run specialist research, risk, and architecture agents in parallel, then synthesize an executive-ready recommendation.</p>",
    unsafe_allow_html=True,
)

st.info(
    "This demo makes four model calls per run: research, risk, architecture, and synthesis."
)

question = st.text_area(
    "Question",
    placeholder="Example: Should we adopt OpenAI Agents SDK for a customer-facing architecture advisory workflow?",
    height=120,
    key="question",
)

left, right = st.columns([1, 3])
with left:
    run = st.button("Run analysis", type="primary", use_container_width=True)
with right:
    st.caption(f"Next run will use `{st.session_state.selected_model}`.")
    st.button("Clear question", on_click=clear_question)

if run:
    validation_error = validate_question(question)
    if validation_error:
        st.warning(validation_error)
    elif not has_openai_api_key():
        st.error("Set OPENAI_API_KEY in .env.local before running the agents.")
    else:
        with st.spinner("Running specialist agents..."):
            try:
                result = asyncio.run(
                    run_research_workflow(
                        question,
                        model=st.session_state.selected_model,
                    )
                )
            except Exception as exc:
                st.error(f"The workflow could not complete: {exc}")
            else:
                st.session_state.last_result = result
                st.session_state.last_question = question

if st.session_state.last_result:
    result = st.session_state.last_result

    st.subheader("Execution Trace")
    st.caption(
        "This local trace shows the orchestrator path for the latest run. "
        "The OpenAI Agents SDK also exports a deeper trace for model calls and spans."
    )
    trace_rows = [
        {
            "Step": event.step,
            "Agent": event.agent,
            "Status": event.status,
            "Elapsed seconds": event.elapsed_seconds,
            "Input tokens": event.token_usage.input_tokens,
            "Output tokens": event.token_usage.output_tokens,
            "Total tokens": event.token_usage.total_tokens,
            "Requests": event.token_usage.requests,
            "Detail": event.detail,
        }
        for event in result.trace_events
    ]
    st.dataframe(trace_rows, use_container_width=True, hide_index=True)
    usage_cols = st.columns(4)
    usage_cols[0].metric("Input tokens", result.metadata["input_tokens"])
    usage_cols[1].metric("Output tokens", result.metadata["output_tokens"])
    usage_cols[2].metric("Total tokens", result.metadata["total_tokens"])
    usage_cols[3].metric("API requests", result.metadata["requests"])
    st.caption(f"OpenAI trace id: `{result.trace_id}`")

    st.subheader("Executive Recommendation")
    st.markdown(result.final_recommendation)

    st.subheader("Specialist Outputs")
    tabs = st.tabs([item.name for item in result.specialist_results])
    for tab, specialist_result in zip(tabs, result.specialist_results):
        with tab:
            if specialist_result.error:
                st.error(specialist_result.error)
            else:
                st.markdown(specialist_result.output)

    with st.expander("Run Metadata"):
        st.json(
            {
                **result.metadata,
                "question": st.session_state.last_question,
            }
        )
