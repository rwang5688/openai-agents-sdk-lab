import os
from pathlib import Path

from dotenv import load_dotenv


DEFAULT_MODEL = "gpt-5.4-mini"

SUPPORTED_MODELS = [
    "gpt-5.4-mini",
    "gpt-5.4",
    "gpt-5.5",
]


APP_DIR = Path(__file__).resolve().parents[1]


def load_environment() -> None:
    load_dotenv(APP_DIR / ".env.local")
    load_dotenv()


def get_default_model() -> str:
    load_environment()
    return os.getenv("OPENAI_MODEL", DEFAULT_MODEL)


def get_supported_models() -> list[str]:
    configured_model = get_default_model()
    models = list(SUPPORTED_MODELS)
    if configured_model not in models:
        models.insert(0, configured_model)
    return models


def has_openai_api_key() -> bool:
    load_environment()
    return bool(os.getenv("OPENAI_API_KEY"))
