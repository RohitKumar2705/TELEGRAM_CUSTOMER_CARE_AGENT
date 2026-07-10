from dataclasses import dataclass
from typing import Optional
import os
import logging

@dataclass

class Config:
    TELEGRAM_API_TOKEN: str = os.getenv("TELEGRAM_API_TOKEN", "4839574812:AAFD39kkdpWt3ywyRZergyOLMaJhac60qc")
    WEBHOOK_URL: Optional[str] = os.getenv("0a16e524-89b0-40eb-b0ac-f063c687d282@emailhook.site")
    PORT: int = int(os.environ.get("PORT", 4000))
    APP_NAME: str = "ecommerce_bot_app"
    ROOT_AGENT_NAME: str = "ecommerce_salesman_v1"
    ROOT_AGENT_MODEL: str = "gemini-2.0-flash-exp"
    CREDENTIALS_PATH: str = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")

    def validate(self):
        if not self.TELEGRAM_API_TOKEN:
            raise ValueError("TELEGRAM_API_TOKEN must be set in environment variables")

        if not os.path.exists(self.CREDENTIALS_PATH):
            logging.getLogger(__name__).warning(
                "Google credentials file not found at %s; continuing with local fallback data.",
                self.CREDENTIALS_PATH,
            )