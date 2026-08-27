from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SampleAssessment:
    size: int
    classification: str


@dataclass
class TemporalWeights:
    long_term: float
    medium_term: float
    short_term: float


DEFAULT_TEMPORAL_WEIGHTS = TemporalWeights(
    long_term=0.50,
    medium_term=0.30,
    short_term=0.20,
)


def assess_sample(size: int) -> SampleAssessment:
    if size < 0:
        raise ValueError("Tamanho da amostra não pode ser negativo.")

    if size < 10:
        classification = "INSUFFICIENT"
    elif size < 30:
        classification = "LIMITED"
    else:
        classification = "ADEQUATE"

    return SampleAssessment(
        size=size,
        classification=classification,
    )


def validate_temporal_weights(
    weights: TemporalWeights = DEFAULT_TEMPORAL_WEIGHTS,
) -> None:
    values = (
        weights.long_term,
        weights.medium_term,
        weights.short_term,
    )

    if any(value < 0 for value in values):
        raise ValueError(
            "Pesos temporais não podem ser negativos."
        )

    total = sum(values)

    if abs(total - 1.0) > 1e-9:
        raise ValueError(
            f"Soma dos pesos temporais deve ser 1.0, recebeu {total}."
        )

@dataclass
class QIAssessment:
    score: float
    classification: str


def classify_qi(score: float) -> str:
    if score < 0 or score > 100:
        raise ValueError("QI deve estar entre 0 e 100.")

    if score >= 80:
        return "PREMIUM"

    if score >= 70:
        return "NORMAL"

    if score >= 65:
        return "BORDERLINE"

    return "SKIP"


def calculate_qi(
    data_quality: float,
    relevance: float,
    freshness: float,
    consistency: float,
) -> QIAssessment:
    values = (
        data_quality,
        relevance,
        freshness,
        consistency,
    )

    if any(value < 0 or value > 100 for value in values):
        raise ValueError(
            "Todos os componentes do QI devem estar entre 0 e 100."
        )

    score = (
        data_quality
        + relevance
        + freshness
        + consistency
    ) / 4.0

    return QIAssessment(
        score=score,
        classification=classify_qi(score),
    )


@dataclass
class TemporalAssessment:
    score: float
    long_term: float
    medium_term: float
    short_term: float


def calculate_temporal_score(
    long_term: float,
    medium_term: float,
    short_term: float,
    weights: TemporalWeights = DEFAULT_TEMPORAL_WEIGHTS,
) -> TemporalAssessment:
    values = (
        long_term,
        medium_term,
        short_term,
    )

    if any(value < 0 or value > 100 for value in values):
        raise ValueError(
            "As avaliações temporais devem estar entre 0 e 100."
        )

    validate_temporal_weights(weights)

    score = (
        long_term * weights.long_term
        + medium_term * weights.medium_term
        + short_term * weights.short_term
    )

    return TemporalAssessment(
        score=score,
        long_term=long_term,
        medium_term=medium_term,
        short_term=short_term,
    )
