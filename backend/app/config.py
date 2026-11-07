"""Settings (M1). Frozen contract — change only via PR approved by SKJ."""
from functools import lru_cache
from typing import Literal

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
        enable_decoding=False,
    )

    database_url: str = "postgresql://aegis:aegis@localhost:5432/aegis"
    paypal_mode: Literal["fake", "sandbox", "live"] = "fake"
    paypal_client_id: str = ""
    paypal_client_secret: str = ""
    paypal_webhook_id: str = ""
    llm_provider: Literal["fake", "groq", "gemini", "mistral"] = "fake"
    llm_model: str = ""
    llm_fallbacks: str = ""  # "gemini:gemini-3.5-flash,mistral:mistral-small-latest"
    groq_api_key: str = ""
    gemini_api_key: str = ""
    mistral_api_key: str = ""
    agents_enabled: list[str] = ["collector", "sentinel", "guardian", "defender"]
    approval_threshold_cents: int = 10000
    kill_switch: bool = False
    console_password: str = "dev"
    demo_mode: bool = True

    @field_validator("agents_enabled", mode="before")
    @classmethod
    def _parse_agents(cls, v):
        if isinstance(v, str):
            return [a.strip() for a in v.split(",") if a.strip()]
        return v

    @property
    def llm_fallback_chain(self) -> list[tuple[str, str]]:
        return [tuple(x.strip().split(":", 1)) for x in self.llm_fallbacks.split(",") if x.strip()]

    @model_validator(mode="after")
    def _refuse_live(self) -> "Settings":
        if self.paypal_mode == "live":
            raise ValueError("PAYPAL_MODE=live is refused by AegisFleet (M1). Use sandbox or fake.")
        if self.paypal_mode != "fake" and self.console_password in ("", "dev"):
            raise ValueError("Set a real CONSOLE_PASSWORD when PAYPAL_MODE is not fake.")
        return self


ROUTES = {
    "invoice.sent": "collector",
    "invoice.overdue": "collector",
    "email.received": "sentinel",
    "payment.captured": "guardian",
    "shipment.created": "guardian",
    "delivery.confirmed": "guardian",
    "dispute.created": "defender",
    "dispute.updated": "defender",
}


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()