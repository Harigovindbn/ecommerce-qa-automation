"""Runtime configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass, replace

from dotenv import load_dotenv

SUPPORTED_BROWSERS = {"chrome", "firefox"}


def parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"Expected a boolean value, received: {value!r}")


@dataclass(frozen=True, slots=True)
class Settings:
    """Validated settings shared across the test framework."""

    base_url: str = "https://www.saucedemo.com/"
    browser: str = "chrome"
    headless: bool = True
    remote_url: str | None = None
    explicit_wait_seconds: int = 10

    @classmethod
    def from_env(cls) -> Settings:
        load_dotenv()
        defaults = cls()
        remote_url = os.getenv("SELENIUM_REMOTE_URL", "").strip() or None
        settings = cls(
            base_url=os.getenv("BASE_URL", defaults.base_url).strip(),
            browser=os.getenv("BROWSER", defaults.browser).strip().lower(),
            headless=parse_bool(os.getenv("HEADLESS", str(defaults.headless))),
            remote_url=remote_url,
            explicit_wait_seconds=int(
                os.getenv("EXPLICIT_WAIT_SECONDS", str(defaults.explicit_wait_seconds))
            ),
        )
        return settings.validate()

    def with_overrides(
        self,
        *,
        base_url: str | None = None,
        browser: str | None = None,
        headless: bool | None = None,
        remote_url: str | None = None,
    ) -> Settings:
        updated = replace(
            self,
            base_url=base_url or self.base_url,
            browser=(browser or self.browser).lower(),
            headless=self.headless if headless is None else headless,
            remote_url=self.remote_url if remote_url is None else remote_url or None,
        )
        return updated.validate()

    def validate(self) -> Settings:
        if self.browser not in SUPPORTED_BROWSERS:
            supported = ", ".join(sorted(SUPPORTED_BROWSERS))
            raise ValueError(f"Unsupported browser {self.browser!r}. Choose one of: {supported}")
        if not self.base_url.startswith(("http://", "https://")):
            raise ValueError("BASE_URL must begin with http:// or https://")
        if self.explicit_wait_seconds <= 0:
            raise ValueError("EXPLICIT_WAIT_SECONDS must be greater than zero")
        return self
