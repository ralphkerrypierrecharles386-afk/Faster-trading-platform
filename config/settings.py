"""
Configuration centralisée de la plateforme.
Toutes les valeurs sensibles (identifiants MT5, clés API, etc.) doivent
être définies via variables d'environnement (.env), jamais en dur ici.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "data" / "storage"

load_dotenv(BASE_DIR / ".env")


@dataclass
class MT5Config:
    login: int = int(os.getenv("MT5_LOGIN", "0"))
    password: str = os.getenv("MT5_PASSWORD", "")
    server: str = os.getenv("MT5_SERVER", "")
    path: str = os.getenv("MT5_TERMINAL_PATH", "")
    timeout: int = int(os.getenv("MT5_TIMEOUT_MS", "60000"))


@dataclass
class RiskConfig:
    # % du capital risqué par trade
    risk_per_trade_pct: float = float(os.getenv("RISK_PER_TRADE_PCT", "1.0"))
    # perte max journalière avant coupure automatique
    max_daily_drawdown_pct: float = float(os.getenv("MAX_DAILY_DD_PCT", "3.0"))
    max_open_positions: int = int(os.getenv("MAX_OPEN_POSITIONS", "5"))
    max_lot_size: float = float(os.getenv("MAX_LOT_SIZE", "5.0"))
    min_risk_reward: float = float(os.getenv("MIN_RISK_REWARD", "1.5"))
    default_sl_atr_multiplier: float = float(os.getenv("SL_ATR_MULT", "1.5"))


@dataclass
class DatabaseConfig:
    url: str = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR / 'trading.db'}")


@dataclass
class AppConfig:
    name: str = os.getenv("APP_NAME", "Edit")
    env: str = os.getenv("APP_ENV", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    timezone: str = os.getenv("APP_TIMEZONE", "UTC")
    symbols: list[str] = field(default_factory=lambda: os.getenv(
        "DEFAULT_SYMBOLS", "EURUSD,GBPUSD,XAUUSD"
    ).split(","))
    timeframes: list[str] = field(default_factory=lambda: os.getenv(
        "DEFAULT_TIMEFRAMES", "M5,M15,H1,H4"
    ).split(","))
    mt5: MT5Config = field(default_factory=MT5Config)
    risk: RiskConfig = field(default_factory=RiskConfig)
    db: DatabaseConfig = field(default_factory=DatabaseConfig)


settings = AppConfig()