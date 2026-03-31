"""
Teste Qui-Quadrado de Aderência (Goodness of Fit)

Verifica se uma amostra observada segue uma distribuição
de frequências alegada (uniforme ou com probabilidades definidas).
"""

import numpy as np
from scipy import stats
from dataclasses import dataclass
from typing import Optional


@dataclass
class ResultadoAderencia:
    observadas: list[float]
    esperadas: list[float]
    componentes: list[float]
    qui2_calculado: float
    qui2_critico: float
    graus_liberdade: int
    p_valor: float
    alpha: float
    rejeita_h0: bool
    n: int
    k: int


def executar(
    observadas: list[float],
    probabilidades: Optional[list[float]] = None,
    alpha: float = 0.05,
) -> ResultadoAderencia:
    """
    Parâmetros
    ----------
    observadas    : frequências observadas em cada categoria
    probabilidades: probabilidade esperada de cada categoria.
                    Se None, assume distribuição uniforme (1/k).
    alpha         : nível de significância (padrão 0.05)
    """
    obs = np.array(observadas, dtype=float)
    n   = obs.sum()
    k   = len(obs)

    if probabilidades is None:
        probs = np.full(k, 1.0 / k)
    else:
        probs = np.array(probabilidades, dtype=float)
        if not np.isclose(probs.sum(), 1.0):
            raise ValueError("As probabilidades devem somar 1.")

    esp        = probs * n
    componentes = (obs - esp) ** 2 / esp
    qui2_calc  = componentes.sum()
    gl         = k - 1
    qui2_crit  = stats.chi2.ppf(1 - alpha, df=gl)
    p_valor    = 1 - stats.chi2.cdf(qui2_calc, df=gl)

    return ResultadoAderencia(
        observadas=obs.tolist(),
        esperadas=esp.tolist(),
        componentes=componentes.tolist(),
        qui2_calculado=round(qui2_calc, 4),
        qui2_critico=round(qui2_crit, 4),
        graus_liberdade=gl,
        p_valor=round(p_valor, 6),
        alpha=alpha,
        rejeita_h0=bool(p_valor <= alpha),
        n=int(n),
        k=k,
    )
