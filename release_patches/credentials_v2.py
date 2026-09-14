from __future__ import annotations
import os

SERVICE = "SHADOW_AI"
_SESSION_KEYS = {}

ENV_NAMES = {
    "gemini": "GEMINI_API_KEY",
    "openai": "OPENAI_API_KEY",
    "elevenlabs": "ELEVENLABS_API_KEY",
}


def _embedded_api_key(provider):
    try:
        from ai.embedded_credentials import EMBEDDED_API_KEYS
        value = EMBEDDED_API_KEYS.get(str(provider or "").lower(), "")
        return str(value or "").strip()
    except Exception:
        return ""


def get_api_key(provider):
    provider = str(provider or "").lower()
    if _SESSION_KEYS.get(provider):
        return _SESSION_KEYS[provider]

    env_name = ENV_NAMES.get(provider)
    if env_name:
        value = os.getenv(env_name, "").strip()
        if value:
            return value

    try:
        import keyring
        value = keyring.get_password(SERVICE, provider)
        if value:
            return value.strip()
    except Exception:
        pass

    return _embedded_api_key(provider)


def save_api_key(provider, api_key, persist=True):
    provider = str(provider or "").lower()
    api_key = str(api_key or "").strip()
    if not provider:
        raise ValueError("Provider is required.")
    if not api_key:
        _SESSION_KEYS.pop(provider, None)
        try:
            import keyring
            keyring.delete_password(SERVICE, provider)
        except Exception:
            pass
        return True
    _SESSION_KEYS[provider] = api_key
    if not persist:
        return True
    try:
        import keyring
        keyring.set_password(SERVICE, provider, api_key)
        return True
    except Exception:
        return False


def has_api_key(provider):
    return bool(get_api_key(provider))
