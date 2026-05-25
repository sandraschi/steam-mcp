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
