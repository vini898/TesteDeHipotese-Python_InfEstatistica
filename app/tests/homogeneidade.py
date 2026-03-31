"""
Teste Qui-Quadrado de Homogeneidade

Verifica se k populações diferentes têm a mesma proporção
de uma característica. Amostras são coletadas separadamente
de cada população.

A mecânica de cálculo é idêntica ao teste de independência;
a diferença está na interpretação e no delineamento do estudo.
"""

import numpy as np
from scipy import stats
from dataclasses import dataclass


@dataclass
class ResultadoHomogeneidade:
    observadas: list[list[float]]
    esperadas: list[list[float]]
    componentes: list[list[float]]
    qui2_calculado: float
    qui2_critico: float
    graus_liberdade: int
    p_valor: float
    alpha: float
    rejeita_h0: bool
    n_grupos: int
    n_categorias: int
    total_geral: int
    totais_grupos: list[int]
    totais_categorias: list[int]


def executar(
    tabela: list[list[float]],
    alpha: float = 0.05,
) -> ResultadoHomogeneidade:
    """
    Parâmetros
    ----------
    tabela : matriz onde cada LINHA é um grupo/população
             e cada COLUNA é uma categoria de resultado
    alpha  : nível de significância (padrão 0.05)
    """
    obs = np.array(tabela, dtype=float)
    n_grupos, n_cats = obs.shape

    tot_grupos   = obs.sum(axis=1)
    tot_cats     = obs.sum(axis=0)
    tot_geral    = obs.sum()

    esp          = np.outer(tot_grupos, tot_cats) / tot_geral
    componentes  = (obs - esp) ** 2 / esp
    qui2_calc    = componentes.sum()
    gl           = (n_grupos - 1) * (n_cats - 1)
    qui2_crit    = stats.chi2.ppf(1 - alpha, df=gl)
    p_valor      = 1 - stats.chi2.cdf(qui2_calc, df=gl)

    return ResultadoHomogeneidade(
        observadas=obs.tolist(),
        esperadas=[[round(v, 4) for v in row] for row in esp.tolist()],
        componentes=[[round(v, 4) for v in row] for row in componentes.tolist()],
        qui2_calculado=round(qui2_calc, 4),
        qui2_critico=round(qui2_crit, 4),
        graus_liberdade=gl,
        p_valor=round(p_valor, 6),
        alpha=alpha,
        rejeita_h0=bool(p_valor <= alpha),
        n_grupos=n_grupos,
        n_categorias=n_cats,
        total_geral=int(tot_geral),
        totais_grupos=[int(v) for v in tot_grupos],
        totais_categorias=[int(v) for v in tot_cats],
    )
