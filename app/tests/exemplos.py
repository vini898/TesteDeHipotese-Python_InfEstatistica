"""
Dados dos exemplos extraídos diretamente dos PDFs fornecidos em aula.
Cada exemplo contém: contexto, hipóteses, dados de entrada e resultado esperado.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ExemploAderencia:
    id: str
    titulo: str
    fonte: str          # referência ao PDF
    contexto: str
    h0: str
    h1: str
    alpha: float
    observadas: list[float]
    probabilidades: Optional[list[float]]   # None = uniforme
    rotulos: list[str]
    conclusao: str


@dataclass
class ExemploContingencia:
    id: str
    titulo: str
    fonte: str
    contexto: str
    h0: str
    h1: str
    alpha: float
    tabela: list[list[float]]
    rotulos_linhas: list[str]
    rotulos_colunas: list[str]
    conclusao: str


# ─────────────────────────────────────────────────────────────
# EXEMPLOS — TESTE DE ADERÊNCIA
# ─────────────────────────────────────────────────────────────

EXEMPLOS_ADERENCIA: list[ExemploAderencia] = [

    ExemploAderencia(
        id="digitos_pesos",
        titulo="Últimos Dígitos de Pesos de Homens",
        fonte="PDF Testes Qui-Quadrado — Exemplo 1",
        contexto=(
            "Quando pessoas MEDEM seu peso, os últimos dígitos "
            "tendem a se distribuir de forma uniforme (0 a 9). "
            "Quando RELATAM, tendem a arredondar para 0 ou 5. "
            "Os dados abaixo são os últimos dígitos dos pesos (lb) "
            "de homens, coletados pelo National Center for Health Statistics. "
            "Queremos testar se esses dígitos ocorrem com a mesma frequência."
        ),
        h0="Os últimos dígitos ocorrem com a mesma frequência (distribuição uniforme).",
        h1="Pelo menos um dígito ocorre com frequência diferente das demais.",
        alpha=0.05,
        observadas=[1175, 44, 169, 111, 112, 731, 96, 110, 171, 65],
        probabilidades=None,   # uniforme: E = n/k
        rotulos=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
        conclusao=(
            "χ² calculado ≈ 4490,17 >> χ² crítico ≈ 16,92. "
            "REJEITAMOS H₀. Os dígitos 0 e 5 concentram a maioria das frequências, "
            "indicando que os pesos foram RELATADOS, não medidos."
        ),
    ),

    ExemploAderencia(
        id="lei_benford",
        titulo="Lei de Benford — Detecção de Invasões Cibernéticas",
        fonte="PDF Testes Qui-Quadrado — Exemplo 2",
        contexto=(
            "A Lei de Benford descreve a distribuição esperada dos dígitos líderes "
            "em conjuntos de dados naturais (populações, preços, tempos de rede). "
            "Agências de segurança usam essa lei para detectar fraudes e ataques "
            "cibernéticos: tráfego normal segue Benford; desvios significativos "
            "podem indicar ataque. Abaixo estão 271 dígitos líderes de tempos "
            "entre chegadas de pacotes de internet."
        ),
        h0="Os dígitos líderes seguem a distribuição dada pela Lei de Benford.",
        h1="Pelo menos uma proporção difere da Lei de Benford.",
        alpha=0.05,
        observadas=[69, 40, 42, 26, 25, 16, 16, 17, 20],
        probabilidades=[0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046],
        rotulos=["1", "2", "3", "4", "5", "6", "7", "8", "9"],
        conclusao=(
            "χ² calculado ≈ 11,28 < χ² crítico ≈ 15,51. "
            "NÃO REJEITAMOS H₀. Os dígitos líderes se ajustam à Lei de Benford, "
            "não há evidência de ataque cibernético nos dados."
        ),
    ),
]


# ─────────────────────────────────────────────────────────────
# EXEMPLOS — TESTE DE INDEPENDÊNCIA
# ─────────────────────────────────────────────────────────────

EXEMPLOS_INDEPENDENCIA: list[ExemploContingencia] = [

    ExemploContingencia(
        id="vacina_autismo",
        titulo="Vacina Tríplice e Autismo",
        fonte="PDF Testes Qui-Quadrado — Exemplo 3 (Parte 1)",
        contexto=(
            "Um estudo investigou se existe relação entre a vacinação tríplice "
            "(sarampo, caxumba e rubéola) e o desenvolvimento de autismo em crianças. "
            "Os dados são provenientes do National Center for Health Statistics. "
            "A tabela mostra a contagem de sujeitos divididos entre vacinados/não vacinados "
            "e com/sem diagnóstico de autismo."
        ),
        h0="O autismo é INDEPENDENTE da vacinação tríplice.",
        h1="O autismo e a vacinação tríplice são DEPENDENTES.",
        alpha=0.05,
        tabela=[
            [25,  64],
            [362, 1427],
        ],
        rotulos_linhas=["Com Autismo", "Sem Autismo"],
        rotulos_colunas=["Não Vacinado", "Vacinado"],
        conclusao=(
            "χ² calculado ≈ 3,20 < χ² crítico ≈ 3,84. "
            "NÃO REJEITAMOS H₀. Não há evidência suficiente de dependência "
            "entre a vacina tríplice e o autismo, com 95% de confiança."
        ),
    ),
]


# ─────────────────────────────────────────────────────────────
# EXEMPLOS — TESTE DE HOMOGENEIDADE
# ─────────────────────────────────────────────────────────────

EXEMPLOS_HOMOGENEIDADE: list[ExemploContingencia] = [

    ExemploContingencia(
        id="carteira_perdida",
        titulo="Experimento da Carteira Perdida — 16 Cidades",
        fonte="PDF Testes Qui-Quadrado — Exemplo 3 (Parte 2)",
        contexto=(
            "A Reader's Digest realizou um experimento perdendo intencionalmente "
            "12 carteiras em cada uma de 16 cidades diferentes ao redor do mundo "
            "(Nova York, Londres, Amsterdã e outras). "
            "Queremos verificar se a proporção de carteiras devolvidas é a MESMA "
            "em todas as cidades, ou se o comportamento varia significativamente."
        ),
        h0="A proporção de carteiras devolvidas é IGUAL nas 16 cidades.",
        h1="A proporção de carteiras devolvidas DIFERE entre pelo menos duas cidades.",
        alpha=0.05,
        tabela=[
            [8, 4], [5, 7], [7, 5], [11, 1],
            [5, 7], [8, 4], [6, 6], [7,  5],
            [3, 9], [1,11], [4, 8], [2, 10],
            [4, 8], [6, 6], [4, 8], [9,  3],
        ],
        rotulos_linhas=["Cidade A","Cidade B","Cidade C","Cidade D",
                        "Cidade E","Cidade F","Cidade G","Cidade H",
                        "Cidade I","Cidade J","Cidade K","Cidade L",
                        "Cidade M","Cidade N","Cidade O","Cidade P"],
        rotulos_colunas=["Devolvida", "Não Devolvida"],
        conclusao=(
            "χ² calculado ≈ 35,39 > χ² crítico ≈ 24,99. "
            "REJEITAMOS H₀. A taxa de devolução não é homogênea: "
            "há diferença significativa de comportamento entre as cidades."
        ),
    ),
]
