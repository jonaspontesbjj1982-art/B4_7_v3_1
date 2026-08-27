# B4.7 v3.1 — Pré + Live

Projeto inicial do motor B4.7 v3.1 Definitive Edition.

## Arquitetura

- `b47/core.py` — motor matemático B4.7.
- `b47/api_football.py` — adaptador para API-Football.
- `b47/database.py` — SQLite para histórico.
- `app.py` — painel Streamlit.
- `config.example.env` — configuração da API.
- `requirements.txt` — dependências.
- `tests/test_core.py` — testes básicos do motor.

## O que já está implementado

1. Truncamento individual 3.5 antes das médias.
2. Liquidity e leakage.
3. Game State μ.
4. Poisson 0..9.
5. Dixon-Coles conforme regra B4.7 quando λ_total < 2.2.
6. Under/Over 2.5.
7. De-Vig.
8. Edge e EV.
9. Stress test λ_total ±0.15 preservando proporção Home/Away.
10. Validação matemática.
11. Classificação ROBUST/FRAGILE.
12. Stake normal/metade/zero.
13. Interface inicial para PRÉ e LIVE.
14. Banco SQLite para registrar análises.
15. Adaptador para API-Football: fixtures, live fixtures, odds e estatísticas.

## Importante

O programa NÃO inventa GF/GC, odds, μ ou horários.

A API-Football fornece fixtures, livescore, eventos, estatísticas, odds pré-jogo e odds in-play no plano gratuito atual, com limite de 100 requisições/dia. Consulte a documentação oficial antes de colocar o monitoramento live em produção.

## Como executar

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
cp config.example.env .env
streamlit run app.py
```

Para usar API-Football, coloque sua chave em `API_FOOTBALL_KEY`.

## Próxima fase recomendada

- conectar automaticamente métricas históricas de equipes;
- mapear IDs dos mercados O/U 2.5 de cada bookmaker;
- implementar captura periódica de snapshots de odds live;
- criar alertas;
- registrar automaticamente o resultado final;
- produzir relatório de acerto, ROI, Edge e EV por liga e por modo (PRÉ/LIVE).
