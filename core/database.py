"""
Couche base de données (SQLAlchemy). Stocke : trades, signaux, équité,
logs de risque, résultats de backtests, watchlist d'entreprises.
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey,
    create_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

from config.settings import settings

Base = declarative_base()


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True)
    symbol = Column(String(20), index=True, nullable=False)
    direction = Column(String(4), nullable=False)  # BUY / SELL
    volume = Column(Float, nullable=False)
    entry_price = Column(Float, nullable=False)
    sl = Column(Float, nullable=True)
    tp = Column(Float, nullable=True)
    exit_price = Column(Float, nullable=True)
    pnl = Column(Float, nullable=True)
    open_time = Column(DateTime, default=dt.datetime.utcnow)
    close_time = Column(DateTime, nullable=True)
    strategy = Column(String(50), nullable=True)
    setup_type = Column(String(50), nullable=True)  # BOS, CHoCH, OB, FVG...
    is_backtest = Column(Boolean, default=False)
    comment = Column(Text, nullable=True)


class Signal(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True)
    symbol = Column(String(20), index=True, nullable=False)
    timeframe = Column(String(5), nullable=False)
    setup_type = Column(String(50), nullable=False)
    direction = Column(String(4), nullable=False)
    price = Column(Float, nullable=False)
    detected_at = Column(DateTime, default=dt.datetime.utcnow)
    confidence = Column(Float, nullable=True)
    metadata_json = Column(Text, nullable=True)


class EquitySnapshot(Base):
    __tablename__ = "equity_snapshots"

    id = Column(Integer, primary_key=True)
    balance = Column(Float, nullable=False)
    equity = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=dt.datetime.utcnow)


class RiskEvent(Base):
    __tablename__ = "risk_events"

    id = Column(Integer, primary_key=True)
    event_type = Column(String(50), nullable=False)
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=dt.datetime.utcnow)


class CompanyWatch(Base):
    __tablename__ = "company_watch"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    ticker = Column(String(20), nullable=True)
    sector = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    score = Column(Float, nullable=True)
    updated_at = Column(DateTime, default=dt.datetime.utcnow)


engine = create_engine(
    settings.db.url, echo=False, future=True,
    connect_args={"check_same_thread": False} if settings.db.url.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, future=True)


def init_db() -> None:
    """Crée toutes les tables si elles n'existent pas déjà. Idempotent :
    peut être appelée à chaque démarrage de l'application sans risque."""
    if settings.db.url.startswith("sqlite:///"):
        db_path = Path(settings.db.url.replace("sqlite:///", ""))
        if db_path.parent != Path(""):
            db_path.parent.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(engine)


def get_session():
    return SessionLocal()


# ---------------------------------------------------------------------
# Requêtes utilitaires courantes (évite de dupliquer les requêtes SQLAlchemy
# ad hoc dans le dashboard, l'exécution et les tests)
# ---------------------------------------------------------------------

def get_open_trades(session, symbol: str | None = None) -> list[Trade]:
    """Trades sans close_time (positions considérées ouvertes)."""
    query = session.query(Trade).filter(Trade.close_time.is_(None))
    if symbol:
        query = query.filter(Trade.symbol == symbol)
    return query.all()


def get_recent_signals(session, limit: int = 50, symbol: str | None = None) -> list[Signal]:
    query = session.query(Signal).order_by(Signal.detected_at.desc())
    if symbol:
        query = query.filter(Signal.symbol == symbol)
    return query.limit(limit).all()


def record_equity_snapshot(session, balance: float, equity: float) -> EquitySnapshot:
    """Enregistre un point de courbe d'équité et le retourne. Ne fait pas
    de commit : à l'appelant de le faire (permet de grouper avec d'autres
    écritures dans la même transaction si besoin)."""
    snap = EquitySnapshot(balance=balance, equity=equity)
    session.add(snap)
    return snap


def record_risk_event(session, event_type: str, details: str = "") -> RiskEvent:
    event = RiskEvent(event_type=event_type, details=details)
    session.add(event)
    return event