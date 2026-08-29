from __future__ import annotations

from math import isfinite


def validate_probability(probability: float) -> float:
    """
    Valida e normaliza uma probabilidade para o intervalo (0, 1].

    Probabilidades 0 ou negativas não permitem calcular uma odd justa.
    Probabilidades acima de 1 são inválidas.
    """
    try:
        value = float(probability)
    except (TypeError, ValueError) as exc:
        raise ValueError("probability must be numeric") from exc

    if not isfinite(value):
        raise ValueError("probability must be finite")

    if value <= 0.0:
        raise ValueError("probability must be greater than 0")

    if value > 1.0:
        raise ValueError("probability must be less than or equal to 1")

    return value


def fair_odd_from_probability(probability: float) -> float:
    """
    Converte probabilidade em odd justa.

    Fórmula:
        fair_odd = 1 / probability
    """
    probability = validate_probability(probability)
    return 1.0 / probability


def fair_probability_from_odd(odd: float) -> float:
    """
    Converte odd decimal em probabilidade implícita bruta.

    Importante:
    esta função NÃO remove margem da casa.
    Para isso, o processo de de-vig deve ser aplicado separadamente.
    """
    try:
        value = float(odd)
    except (TypeError, ValueError) as exc:
        raise ValueError("odd must be numeric") from exc

    if not isfinite(value):
        raise ValueError("odd must be finite")

    if value <= 1.0:
        raise ValueError("odd must be greater than 1")

    return 1.0 / value
