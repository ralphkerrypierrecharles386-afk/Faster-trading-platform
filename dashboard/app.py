"""
Tableau de bord Streamlit — "Edit"
Vue d'ensemble compte, positions ouvertes, historique de trades, courbe
d'équité, signaux détectés par le moteur d'analyse.

Lancer avec : streamlit run dashboard/app.py
"""
import datetime as dt
from pathlib import Path

import pandas as pd
import streamlit as st

from core.database import (
    init_db, get_session, Trade, EquitySnapshot, Signal,
)

ASSETS_DIR = Path(__file__).parent / "assets"
APP_NAME = "Edit"

st.set_page_config(
    page_title=APP_NAME,
    page_icon=str(ASSETS_DIR / "icon.png") if (ASSETS_DIR / "icon.png").exists() else "📈",
    layout="wide",
)

# ---------------------------------------------------------------------
# En-tête : logo + message de bienvenue
# ---------------------------------------------------------------------
header_col1, header_col2 = st.columns([3, 2])
with header_col1:
    if (ASSETS_DIR / "logo_banner.png").exists():
        st.image(str(ASSETS_DIR / "logo_banner.png"), use_container_width=True)
    else:
        st.title(APP_NAME)
with header_col2:
    hour = dt.datetime.now().hour
    if hour < 12:
        greeting = "Bonjour"
    elif hour < 18:
        greeting = "Bon après-midi"
    else:
        greeting = "Bonsoir"
    st.markdown(
        f"""
        <div style="height:100%; display:flex; flex-direction:column;
                    justify-content:center; padding-left:1.5rem;">
          <h3 style="margin-bottom:0.2rem;">{greeting} 👋</h3>
          <p style="color:#94a3b8; font-size:0.95rem;">
            Bienvenue sur <b>{APP_NAME}</b> — votre poste de pilotage pour
            le trading algorithmique : signaux détectés, performance de
            vos stratégies et suivi du risque, en un coup d'œil.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

init_db()
session = get_session()

col1, col2, col3, col4 = st.columns(4)
trades = session.query(Trade).all()
closed = [t for t in trades if t.pnl is not None]
wins = [t for t in closed if t.pnl > 0]

col1.metric("Trades totaux", len(trades))
col2.metric("Trades clôturés", len(closed))
col3.metric("Winrate", f"{(len(wins)/len(closed)*100):.1f}%" if closed else "—")
col4.metric("PnL net", f"{sum(t.pnl for t in closed):.2f}" if closed else "0.00")

st.subheader("Courbe d'équité")
equity = session.query(EquitySnapshot).order_by(EquitySnapshot.timestamp).all()
if equity:
    df_eq = pd.DataFrame([{"time": e.timestamp, "equity": e.equity} for e in equity])
    st.line_chart(df_eq.set_index("time"))
else:
    st.info("Aucune donnée d'équité pour le moment.")

st.subheader("Derniers signaux détectés")
signals = session.query(Signal).order_by(Signal.detected_at.desc()).limit(50).all()
if signals:
    st.dataframe(pd.DataFrame([{
        "Symbole": s.symbol, "TF": s.timeframe, "Setup": s.setup_type,
        "Direction": s.direction, "Prix": s.price, "Détecté le": s.detected_at,
    } for s in signals]))
else:
    st.info("Aucun signal en base pour le moment.")

st.subheader("Historique des trades")
if trades:
    st.dataframe(pd.DataFrame([{
        "Symbole": t.symbol, "Direction": t.direction, "Volume": t.volume,
        "Entrée": t.entry_price, "Sortie": t.exit_price, "PnL": t.pnl,
        "Stratégie": t.strategy, "Setup": t.setup_type,
        "Ouvert le": t.open_time, "Fermé le": t.close_time,
    } for t in trades]))
else:
    st.info("Aucun trade en base pour le moment.")