"""Loads environment variables from almog_work/.env and provides an Azure OpenAI client.

Usage:
    from openai_client import get_openai_client
    client = get_openai_client()
    response = client.chat.completions.create(...)

Credentials are read from almog_work/.env (git-ignored, never committed):
    AZURE_OPENAI_API_KEY
    AZURE_OPENAI_ENDPOINT
    AZURE_OPENAI_DEPLOYMENT
    AZURE_OPENAI_API_VERSION (defaults to 2024-05-01-preview)
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AzureOpenAI

_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH)

_client = None


def get_openai_client():
    """Return a cached AzureOpenAI client built from AZURE_OPENAI_* env vars."""
    global _client

    if _client is None:
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-05-01-preview")

        missing = [
            name
            for name, value in [
                ("AZURE_OPENAI_API_KEY", api_key),
                ("AZURE_OPENAI_ENDPOINT", endpoint),
            ]
            if not value
        ]
        if missing:
            raise ValueError(
                f"Missing required env var(s) {missing} in {_ENV_PATH}."
            )

        # If a Foundry *project* endpoint was provided (.../api/projects/<name>),
        # strip it down to the resource root, since key-based auth via AzureOpenAI
        # only works against the base resource endpoint, not the project path.
        if "/api/projects/" in endpoint:
            endpoint = endpoint.split("/api/projects/")[0]

        _client = AzureOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint,
            api_version=api_version,
        )

    return _client


GPT_MODEL = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-5.1")


def run_gpt_chat(messages, max_new_tokens=1500):
    """Run a chat-style completion via Azure OpenAI and return only the generated text.

    Same signature/return shape as local_granite_client.run_granite_chat, so the two
    can be swapped interchangeably as the `chat_fn` passed to extraction/validation agents.
    """
    client = get_openai_client()
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=messages,
        max_completion_tokens=max_new_tokens,
    )
    return (response.choices[0].message.content or "").strip()
