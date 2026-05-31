import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Settings:
    steam_api_key: str = field(default_factory=lambda: os.getenv("STEAM_API_KEY", ""))
    steam_id: str = field(default_factory=lambda: os.getenv("STEAM_ID", ""))
    host: str = field(default_factory=lambda: os.getenv("HOST", "127.0.0.1"))
    backend_port: int = field(default_factory=lambda: int(os.getenv("BACKEND_PORT", "11020")))
    frontend_port: int = field(default_factory=lambda: int(os.getenv("FRONTEND_PORT", "11021")))
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "warning"))
    steamcmd_path: str = field(default_factory=lambda: os.getenv("STEAMCMD_PATH", ""))
    prefab_apps: bool = field(
        default_factory=lambda: os.getenv("STEAM_PREFAB_APPS", "1").strip().lower() not in ("0", "false", "no")
    )
    chat_mode: str = field(default_factory=lambda: os.getenv("STEAM_CHAT_MODE", "hybrid").strip().lower())
    ai_provider: str = field(default_factory=lambda: os.getenv("AI_PROVIDER", "ollama").strip().lower())
    ai_endpoint: str = field(
        default_factory=lambda: os.getenv(
            "AI_ENDPOINT",
            os.getenv("STEAM_SAMPLING_BASE_URL", "http://127.0.0.1:11434/v1/chat/completions"),
        )
    )
    ai_model: str = field(default_factory=lambda: os.getenv("AI_MODEL", "llama3.1:8b"))

    @property
    def has_api_key(self) -> bool:
        return bool(self.steam_api_key)

    @property
    def has_steam_id(self) -> bool:
        return bool(self.steam_id)

    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parent.parent.parent


settings = Settings()
