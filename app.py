from datetime import datetime, timedelta, timezone
import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from b47.core import B47Input, analyze_b47
from b47.database import init_db, recent, save_analysis
from b47.api_football import APIFootball

load_dotenv()

st.set_page_config(page_title="B4.7 v3.1", layout="wide")
st.title("B4.7 v3.1 — Pré + Live")
st.caption("Motor único: truncamento 3.5 → λ → Poisson → Dixon-Coles → O/U → De-Vig → Edge/EV → Stress → validação.")

db_path = os.getenv("DB_PATH", "b47.db")
init_db(db_path)

with st.sidebar:
    st.header("Configuração")
    api_key = st.text_input("API-Football key", value=os.getenv("API_FOOTBALL_KEY", ""), type="password")
    base_url = os.getenv("API_FOOTBALL_BASE_URL", "https://v3.football.api-sports.io")
    st.caption("A chave não é exibida no painel.")
    st.divider()
    mode = st.radio("Modo", ["PRÉ", "LIVE"])

tab1, tab2, tab3 = st.tabs(["Analisar", "API", "Histórico"])

with tab1:
    st.subheader(f"Análise {mode}")
    c1, c2 = st.columns(2)

    with c1:
        home = st.text_input("Home", "Home")
        away = st.text_input("Away", "Away")
        home_gf = st.number_input("Home GF", min_value=0.0, value=1.5, step=0.1)
        home_gc = st.number_input("Home GC", min_value=0.0, value=1.2, step=0.1)
        away_gf = st.number_input("Away GF", min_value=0.0, value=1.3, step=0.1)
        away_gc = st.number_input("Away GC", min_value=0.0, value=1.4, step=0.1)

    with c2:
        odd_over = st.number_input("Odd Over 2.5", min_value=1.01, value=2.00, step=0.01)
        odd_under = st.number_input("Odd Under 2.5", min_value=1.01, value=1.80, step=0.01)
        mu = st.number_input("μ Game State", min_value=0.01, value=1.00, step=0.01)
        now = datetime.now()
        if mode == "PRÉ":
            start = st.datetime_input("Start", value=now + timedelta(hours=2))
            prediction = st.datetime_input("Prediction", value=now)
        else:
            start = st.datetime_input("Start", value=now - timedelta(minutes=35))
            prediction = st.datetime_input("Prediction", value=now)
        fixture_id = st.text_input("Fixture ID (opcional)")

    if st.button("Executar B4.7", type="primary"):
        inp = B47Input(
            home_gf=home_gf, home_gc=home_gc,
            away_gf=away_gf, away_gc=away_gc,
            odd_over=odd_over, odd_under=odd_under,
            mu=mu, start_time=start, prediction_time=prediction,
            mode=mode,
        )
        result = analyze_b47(inp)
        st.session_state["last_result"] = result
        if result.get("status") not in ("MISSING INPUT", "INVALID", "INVALID CALCULATION"):
            save_analysis(
                db_path, result, mode=mode, fixture_id=fixture_id or None,
                home=home, away=away,
                start_time=str(start), prediction_time=str(prediction)
            )

    result = st.session_state.get("last_result")
    if result:
        st.divider()
        st.subheader("B4.7 RESULT v3.1")
        st.metric("DECISÃO", result.get("status", "—"))
        if result.get("status") in ("MISSING INPUT", "INVALID", "INVALID CALCULATION"):
            st.error(result)
        else:
            a, b, c, d = st.columns(4)
            a.metric("P Under 2.5", f"{result['probabilities']['under_2_5']*100:.2f}%")
            b.metric("P Over 2.5", f"{result['probabilities']['over_2_5']*100:.2f}%")
            c.metric("Edge Over", f"{result['edge_ev']['over']['edge']*100:.2f}%")
            d.metric("EV Over", f"{result['edge_ev']['over']['ev']*100:.2f}%")

            st.write("**Liquidez:**", f"{result['liquidity_hours']:.2f} h — {result['liquidity_status']}")
            st.write("**Leakage:**", result["leakage"])
            st.write("**Dixon-Coles:**", result["dixon_coles"])
            st.write("**Fragilidade:**", result["fragility"])
            st.write("**Stake:**", result["stake"])
            st.json(result)

with tab2:
    st.subheader("API-Football")
    if not api_key:
        st.info("Coloque a chave no campo da barra lateral para consultar a API.")
    else:
        api = APIFootball(api_key, base_url)
        q1, q2 = st.columns(2)
        with q1:
            date = st.date_input("Data", value=datetime.now().date())
            if st.button("Buscar jogos do dia"):
                try:
                    data = api.fixtures_by_date(str(date))
                    rows = []
                    for item in data.get("response", []):
                        fx = item["fixture"]
                        teams = item["teams"]
                        goals = item["goals"]
                        rows.append({
                            "fixture_id": fx["id"],
                            "status": fx["status"]["short"],
                            "minute": fx["status"].get("elapsed"),
                            "home": teams["home"]["name"],
                            "away": teams["away"]["name"],
                            "home_goals": goals["home"],
                            "away_goals": goals["away"],
                        })
                    st.dataframe(pd.DataFrame(rows), use_container_width=True)
                except Exception as e:
                    st.error(str(e))
        with q2:
            if st.button("Buscar jogos LIVE"):
                try:
                    data = api.live_fixtures()
                    rows = []
                    for item in data.get("response", []):
                        fx = item["fixture"]
                        teams = item["teams"]
                        goals = item["goals"]
                        rows.append({
                            "fixture_id": fx["id"],
                            "status": fx["status"]["short"],
                            "minute": fx["status"].get("elapsed"),
                            "home": teams["home"]["name"],
                            "away": teams["away"]["name"],
                            "home_goals": goals["home"],
                            "away_goals": goals["away"],
                        })
                    st.dataframe(pd.DataFrame(rows), use_container_width=True)
                except Exception as e:
                    st.error(str(e))

with tab3:
    st.subheader("Histórico B4.7")
    cols, rows = recent(db_path, 200)
    if rows:
        st.dataframe(pd.DataFrame(rows, columns=cols), use_container_width=True)
    else:
        st.info("Ainda não há análises registradas.")
