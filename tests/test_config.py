"""Fast unit tests for framework configuration."""

import pytest

from ecommerce_qa.config import Settings, parse_bool


@pytest.mark.parametrize(("raw_value", "expected"), [("true", True), ("YES", True), ("0", False)])
def test_boolean_environment_values(raw_value: str, expected: bool) -> None:
    assert parse_bool(raw_value) is expected


def test_invalid_boolean_is_rejected() -> None:
    with pytest.raises(ValueError, match="Expected a boolean"):
        parse_bool("sometimes")


def test_unsupported_browser_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unsupported browser"):
        Settings(browser="safari").validate()


def test_non_positive_wait_is_rejected() -> None:
    with pytest.raises(ValueError, match="greater than zero"):
        Settings(explicit_wait_seconds=0).validate()
