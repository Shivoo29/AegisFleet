"""M1 config tests."""
import pytest

from app.config import Settings, get_settings


def test_live_mode_raises() -> None:
    with pytest.raises(Exception):
        Settings(paypal_mode="live")


def test_agents_enabled_parsed_from_csv() -> None:
    s = Settings(agents_enabled="collector,sentinel")
    assert s.agents_enabled == ["collector", "sentinel"]


def test_get_settings_cached() -> None:
    assert get_settings() is get_settings()