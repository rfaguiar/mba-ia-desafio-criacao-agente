import pytest

from aurora.config import Settings


def test_default_database_is_local_and_not_in_memory() -> None:
    config = Settings(_env_file=None, GOOGLE_API_KEY="test-key")

    assert config.database_url.startswith("sqlite+aiosqlite:///")
    assert ":memory:" not in config.database_url


def test_google_api_key_is_required_only_when_agent_runs() -> None:
    config = Settings(_env_file=None)

    assert config.google_api_key is None
    with pytest.raises(ValueError, match="GOOGLE_API_KEY"):
        config.require_google_api_key()


def test_environment_values_are_loaded() -> None:
    config = Settings(
        _env_file=None,
        GOOGLE_API_KEY="secret-test-key",
        GEMINI_MODEL="gemini-test",
        DATABASE_URL="sqlite+aiosqlite:///./custom.db",
    )

    assert config.require_google_api_key() == "secret-test-key"
    assert config.gemini_model == "gemini-test"
    assert config.database_url.endswith("custom.db")

