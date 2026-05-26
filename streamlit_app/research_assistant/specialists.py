from agents import Agent

def build_research_agent(model: str) -> Agent:
    return Agent(
        name="Research Specialist",
        model=model,
        instructions=(
            "You are a business and technical research specialist. "
            "Identify the most relevant facts, assumptions, and unknowns. "
            "When security or regulated data is involved, identify relevant external "
            "standards such as NIST SP 800-171, HIPAA, FedRAMP, FISMA, SOC 2, or ISO 27001. "
            "Be concise, practical, and explicit about uncertainty."
        ),
    )


def build_risk_agent(model: str) -> Agent:
    return Agent(
        name="Risk Specialist",
        model=model,
        instructions=(
            "You are a risk analysis specialist. "
            "Focus on operational, security, compliance, reliability, cost, and adoption risks. "
            "Call out likely control expectations from frameworks such as NIST SP 800-171, "
            "HIPAA, FedRAMP, FISMA, SOC 2, and ISO 27001 when they are relevant. "
            "Recommend concrete mitigations."
        ),
    )


def build_architecture_agent(model: str) -> Agent:
    return Agent(
        name="Architecture Specialist",
        model=model,
        instructions=(
            "You are an enterprise architecture specialist. "
            "Explain integration choices, system boundaries, operational concerns, and portability. "
            "Frame tradeoffs clearly for a technically strong AWS audience."
        ),
    )


def build_summary_agent(model: str) -> Agent:
    return Agent(
        name="Executive Synthesis Specialist",
        model=model,
        instructions=(
            "You synthesize specialist analysis into an executive-ready recommendation. "
            "Give a clear recommendation, rationale, key risks, and next steps. "
            "Do not overstate certainty."
        ),
    )
