import os

API_KEY_ENV = "OPENROUTER_API_KEY"
# OpenRouter API key format prefix
API_KEY_PREFIX = "sk-or-v1-"
# Minimum expected key length
MIN_API_KEY_LENGTH = 20


def load_api_key() -> str:
    api_key = os.environ.get(API_KEY_ENV)
    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY not set. Get key at https://openrouter.ai/keys"
        )
    if not api_key.startswith(API_KEY_PREFIX):
        raise ValueError(f"Invalid API key format. Expected: {API_KEY_PREFIX}...")
    if len(api_key) < MIN_API_KEY_LENGTH:
        raise ValueError(
            f"API key too short ({len(api_key)} < {MIN_API_KEY_LENGTH} chars)"
        )
    return api_key
