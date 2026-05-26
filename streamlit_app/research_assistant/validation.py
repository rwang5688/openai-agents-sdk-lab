MAX_QUESTION_CHARS = 4000


def validate_question(question: str) -> str | None:
    if not question.strip():
        return "Enter a question to analyze."

    if len(question) > MAX_QUESTION_CHARS:
        return f"Please keep the question under {MAX_QUESTION_CHARS:,} characters for this demo."

    return None
