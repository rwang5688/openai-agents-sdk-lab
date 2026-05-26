from streamlit_app.research_assistant.validation import MAX_QUESTION_CHARS, validate_question


def test_validate_question_rejects_empty_text():
    assert validate_question("   ") == "Enter a question to analyze."


def test_validate_question_rejects_overly_long_text():
    message = validate_question("x" * (MAX_QUESTION_CHARS + 1))

    assert message is not None
    assert "under 4,000 characters" in message


def test_validate_question_accepts_normal_question():
    assert validate_question("Should we use a multi-agent architecture?") is None
