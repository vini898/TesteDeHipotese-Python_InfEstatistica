"""
Teste Qui-Quadrado de Independência

Verifica se duas variáveis categóricas em uma tabela de
contingência são independentes entre si.
"""

import numpy as np
from scipy import stats
from dataclasses import dataclass


@dataclass
class ResultadoIndependencia:
    observadas: list[list[float]]
    esperadas: list[list[float]]
    componentes: list[list[float]]
    qui2_calculado: float
    qui2_critico: float
    graus_liberdade: int
    p_valor: float
    alpha: float
    rejeita_h0: bool
    n_linhas: int
    n_colunas: int
    total_geral: int
    totais_linhas: list[int]
    totais_colunas: list[int]


def executar(
    tabela: list[list[float]],
    alpha: float = 0.05,
) -> ResultadoIndependencia:
    """
    Parâmetros
    ----------
    tabela : matriz r×c com as frequências observadas
    alpha  : nível de significância (padrão 0.05)
    """
    obs = np.array(tabela, dtype=float)
    r, c = obs.shape

    tot_linhas  = obs.sum(axis=1)
    tot_colunas = obs.sum(axis=0)
    tot_geral   = obs.sum()

    esp         = np.outer(tot_linhas, tot_colunas) / tot_geral
    componentes = (obs - esp) ** 2 / esp
    qui2_calc   = componentes.sum()
    gl          = (r - 1) * (c - 1)
    qui2_crit   = stats.chi2.ppf(1 - alpha, df=gl)
    p_valor     = 1 - stats.chi2.cdf(qui2_calc, df=gl)

    return ResultadoIndependencia(
        observadas=obs.tolist(),
        esperadas=[[round(v, 4) for v in row] for row in esp.tolist()],
        componentes=[[round(v, 4) for v in row] for row in componentes.tolist()],
        qui2_calculado=round(qui2_calc, 4),
        qui2_critico=round(qui2_crit, 4),
        graus_liberdade=gl,
        p_valor=round(p_valor, 6),
        alpha=alpha,
        rejeita_h0=bool(p_valor <= alpha),
        n_linhas=r,
        n_colunas=c,
        total_geral=int(tot_geral),
        totais_linhas=[int(v) for v in tot_linhas],
        totais_colunas=[int(v) for v in tot_colunas],
    )
