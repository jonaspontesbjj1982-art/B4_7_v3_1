from dataclasses import dataclass, field
from typing import Any


@dataclass
class MarketOutcome:
    market: str
    outcome: str
    odd: float
    line: float | None = None
    bookmaker: str | None = None
    timestamp: str | None = None
    liquidity: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Market:
    name: str
    outcomes: list[MarketOutcome] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class MatchContext:
    home_team: str
    away_team: str
    competition: str | None = None
    fixture_id: str | None = None
    start_time: str | None = None
    status: str = "PRE"
    minute: int = 0
    home_goals: int = 0
    away_goals: int = 0
    home_xg: float | None = None
    away_xg: float | None = None
    home_shots: int = 0
    away_shots: int = 0
    home_shots_on_target: int = 0
    away_shots_on_target: int = 0
    home_corners: int = 0
    away_corners: int = 0
    home_cards: int = 0
    away_cards: int = 0
    lineups_confirmed: bool = False
    weather_available: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class DataQuality:
    sample_size: int = 0
    sample_status: str = "INSUFFICIENT"
    q_long: float = 0.50
    q_medium: float = 0.30
    q_short: float = 0.20
    qi: float = 0.0
    notes: list[str] = field(default_factory=list)


@dataclass
class ProbabilityModel:
    statistical: float | None = None
    contextual: float | None = None
    market_fair: float | None = None
    central: float | None = None
    interval_low: float | None = None
    interval_high: float | None = None
    divergence_pp: float | None = None


@dataclass
class ConservativeEstimate:
    probability: float | None = None
    interval_floor: float | None = None
    penalty_total: float = 0.0
    penalties: dict[str, float] = field(default_factory=dict)
    confidence: float = 0.0


@dataclass
class PricingResult:
    fair_odd: float | None = None
    minimum_entry_odd: float | None = None
    offered_odd: float | None = None
    market_fair_probability: float | None = None
    conservative_probability: float | None = None
    edge: float | None = None
    ev: float | None = None
    safety_margin: float | None = None


@dataclass
class RiskResult:
    sample_risk: float = 0.0
    lineup_risk: float = 0.0
    volatility_risk: float = 0.0
    line_sensitivity_risk: float = 0.0
    divergence_risk: float = 0.0
    nobet_score: float = 0.0
    robustness: str = "UNKNOWN"
    stress_tests: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class DecisionResult:
    classification: str = "PULA"
    stake_units: float = 0.0
    reason: str = ""
    correlated: bool = False
    exposure_before: float = 0.0
    exposure_after: float = 0.0


@dataclass
class AuditRecord:
    entry_odd: float | None = None
    closing_odd: float | None = None
    clv: float | None = None
    result: str | None = None
    brier_score: float | None = None
    calibration_error: float | None = None
    out_of_sample: bool | None = None


@dataclass
class B42Analysis:
    event: MatchContext
    selected_market: Market | None = None
    selected_outcome: MarketOutcome | None = None
    mode: str = "PRE"
    p0_status: str = "PENDING"
    data_quality: DataQuality = field(default_factory=DataQuality)
    probability: ProbabilityModel = field(default_factory=ProbabilityModel)
    conservative: ConservativeEstimate = field(default_factory=ConservativeEstimate)
    pricing: PricingResult = field(default_factory=PricingResult)
    risk: RiskResult = field(default_factory=RiskResult)
    decision: DecisionResult = field(default_factory=DecisionResult)
    audit: AuditRecord = field(default_factory=AuditRecord)
    ranking_score: float | None = None
    notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
