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

    # ── EXEMPLOS COTIDIANO BRASILEIRO ────────────────────────

    ExemploAderencia(
        id="acidentes_transito_sp",
        titulo="Acidentes de Trânsito por Dia da Semana — SP",
        fonte="Cotidiano Brasileiro — Transporte",
        contexto=(
            "A CET-SP registrou 1.852 acidentes de trânsito ao longo de uma semana "
            "típica na cidade de São Paulo. Se os acidentes fossem distribuídos "
            "igualmente entre os sete dias, esperaríamos aproximadamente 265 por dia. "
            "Os dados, porém, mostram concentração maior nos finais de semana. "
            "Testamos se a distribuição de acidentes é uniforme ao longo da semana."
        ),
        h0="Os acidentes de trânsito se distribuem igualmente pelos 7 dias da semana.",
        h1="Pelo menos um dia concentra mais acidentes do que os demais.",
        alpha=0.05,
        observadas=[312, 198, 187, 201, 224, 389, 341],
        probabilidades=None,
        rotulos=["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"],
        conclusao=(
            "χ² calculado ≈ 150,09 >> χ² crítico ≈ 12,59. "
            "REJEITAMOS H₀. Os acidentes não são uniformes: "
            "sábado e domingo concentram significativamente mais ocorrências, "
            "o que justifica reforço de fiscalização nos fins de semana."
        ),
    ),

    ExemploAderencia(
        id="meios_pagamento",
        titulo="Meios de Pagamento em Supermercados Brasileiros",
        fonte="Cotidiano Brasileiro — Consumo",
        contexto=(
            "A ABECS (Associação Brasileira das Empresas de Cartões) publicou em 2023 "
            "que a participação esperada dos meios de pagamento no varejo é: "
            "Pix 45%, Débito 25%, Crédito 20% e Dinheiro 10%. "
            "Uma rede de supermercados de Fortaleza registrou 400 transações em um dia "
            "e quer saber se o perfil de seus clientes segue esse padrão nacional."
        ),
        h0="A distribuição de meios de pagamento segue o padrão nacional (Pix 45%, Débito 25%, Crédito 20%, Dinheiro 10%).",
        h1="O perfil de pagamento da loja difere do padrão nacional.",
        alpha=0.05,
        observadas=[198, 87, 62, 53],
        probabilidades=[0.45, 0.25, 0.20, 0.10],
        rotulos=["Pix", "Débito", "Crédito", "Dinheiro"],
        conclusao=(
            "χ² calculado ≈ 11,77 > χ² crítico ≈ 7,81. "
            "REJEITAMOS H₀. O perfil da loja difere do padrão nacional: "
            "o dinheiro tem participação superior ao esperado e o Pix, inferior, "
            "sugerindo que o público local ainda adota menos pagamentos digitais."
        ),
    ),

    ExemploAderencia(
        id="internacoes_sus",
        titulo="Internações Hospitalares por Dia da Semana — SUS",
        fonte="Cotidiano Brasileiro — Saúde",
        contexto=(
            "O DataSUS registrou 920 internações em um hospital público durante "
            "uma semana. Se as internações fossem uniformes, esperaríamos cerca de "
            "131 por dia. Gestores hospitalares querem saber se a demanda varia "
            "ao longo da semana para planejar melhor a escala de profissionais, "
            "especialmente nos finais de semana quando há menos médicos de plantão."
        ),
        h0="As internações se distribuem uniformemente pelos 7 dias da semana.",
        h1="A demanda por internações varia significativamente entre os dias.",
        alpha=0.05,
        observadas=[142, 156, 148, 151, 160, 89, 74],
        probabilidades=None,
        rotulos=["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"],
        conclusao=(
            "χ² calculado ≈ 55,45 >> χ² crítico ≈ 12,59. "
            "REJEITAMOS H₀. As internações caem drasticamente no fim de semana "
            "(sábado e domingo concentram menos casos), possivelmente porque "
            "pacientes evitam hospitais ou buscam UPAs. Isso pode indicar "
            "subatendimento e requer revisão na alocação de recursos."
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

    # ── EXEMPLOS COTIDIANO BRASILEIRO ────────────────────────

    ExemploContingencia(
        id="transporte_renda",
        titulo="Modal de Transporte × Renda Familiar — Região Metropolitana",
        fonte="Cotidiano Brasileiro — Transporte",
        contexto=(
            "Um estudo sobre mobilidade urbana entrevistou 1.054 trabalhadores "
            "de uma região metropolitana brasileira e registrou o principal modal "
            "de transporte utilizado para ir ao trabalho, cruzando com a faixa de "
            "renda familiar. A questão é: a escolha do modal depende da renda, "
            "ou as pessoas escolhem transporte independentemente de quanto ganham?"
        ),
        h0="O modal de transporte utilizado é INDEPENDENTE da faixa de renda familiar.",
        h1="Existe DEPENDÊNCIA entre o modal de transporte e a faixa de renda.",
        alpha=0.05,
        tabela=[
            [210, 85,  32],
            [143, 178, 67],
            [41,  198, 38],
        ],
        rotulos_linhas=["Até 2 sal. mín.", "2 a 5 sal. mín.", "Acima de 5 sal. mín."],
        rotulos_colunas=["Transp. Público", "Carro Próprio", "Moto"],
        conclusao=(
            "χ² calculado ≈ 167,54 >> χ² crítico ≈ 9,49. "
            "REJEITAMOS H₀. Há forte dependência entre renda e modal: "
            "trabalhadores de menor renda usam predominantemente transporte público, "
            "enquanto os de maior renda preferem carro próprio."
        ),
    ),

    ExemploContingencia(
        id="plano_saude_escolaridade",
        titulo="Cobertura de Plano de Saúde × Escolaridade",
        fonte="Cotidiano Brasileiro — Saúde",
        contexto=(
            "A ANS divulgou dados sobre 620 brasileiros entrevistados em uma "
            "pesquisa nacional de saúde. O levantamento cruzou o nível de "
            "escolaridade com a posse de plano de saúde privado. "
            "A questão central é: ter ou não plano de saúde está relacionado "
            "ao nível de escolaridade do indivíduo?"
        ),
        h0="A cobertura de plano de saúde é INDEPENDENTE do nível de escolaridade.",
        h1="Existe DEPENDÊNCIA entre plano de saúde e escolaridade.",
        alpha=0.05,
        tabela=[
            [52,  148],
            [89,  121],
            [163,  47],
        ],
        rotulos_linhas=["Fund. / Médio incomp.", "Médio completo", "Superior completo"],
        rotulos_colunas=["Tem plano", "Não tem plano"],
        conclusao=(
            "χ² calculado ≈ 114,84 >> χ² crítico ≈ 5,99. "
            "REJEITAMOS H₀. Escolaridade e cobertura de saúde são dependentes: "
            "quanto maior a escolaridade, maior a proporção com plano privado. "
            "Isso reflete desigualdade de acesso à saúde no Brasil."
        ),
    ),

    ExemploContingencia(
        id="ultraprocessados_exercicio",
        titulo="Consumo de Ultraprocessados × Frequência de Exercício",
        fonte="Cotidiano Brasileiro — Saúde",
        contexto=(
            "Pesquisadores do IBGE acompanharam 500 adultos e classificaram "
            "cada um quanto ao consumo de alimentos ultraprocessados "
            "(alto ou baixo) e à frequência semanal de atividade física "
            "(sedentário, ativo ou muito ativo). O objetivo é verificar se "
            "quem se exercita mais tende a consumir menos ultraprocessados."
        ),
        h0="O consumo de ultraprocessados é INDEPENDENTE da frequência de exercício.",
        h1="Existe DEPENDÊNCIA entre consumo de ultraprocessados e frequência de exercício.",
        alpha=0.05,
        tabela=[
            [87,  43],
            [61,  79],
            [28, 102],
        ],
        rotulos_linhas=["Sedentário", "Ativo", "Muito ativo"],
        rotulos_colunas=["Alto consumo", "Baixo consumo"],
        conclusao=(
            "χ² calculado ≈ 54,35 >> χ² crítico ≈ 5,99. "
            "REJEITAMOS H₀. Há associação significativa: sedentários consomem "
            "mais ultraprocessados, enquanto pessoas muito ativas têm "
            "predominância de baixo consumo — os hábitos estão correlacionados."
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

    # ── EXEMPLOS COTIDIANO BRASILEIRO ────────────────────────

    ExemploContingencia(
        id="adesao_tratamento_regioes",
        titulo="Adesão a Tratamento Médico por Região do Brasil",
        fonte="Cotidiano Brasileiro — Saúde",
        contexto=(
            "O Ministério da Saúde monitorou a adesão a um programa de "
            "tratamento de hipertensão em cinco regiões brasileiras. "
            "Foram selecionados pacientes aleatoriamente em cada região "
            "e verificado se continuaram o tratamento após 6 meses. "
            "Queremos saber se a taxa de adesão é homogênea entre as regiões "
            "ou se fatores regionais influenciam o abandono do tratamento."
        ),
        h0="A taxa de adesão ao tratamento é IGUAL nas cinco regiões do Brasil.",
        h1="A taxa de adesão DIFERE entre pelo menos duas regiões.",
        alpha=0.05,
        tabela=[
            [134,  66],
            [198, 102],
            [221,  79],
            [312,  88],
            [ 87,  63],
        ],
        rotulos_linhas=["Norte", "Nordeste", "Sul", "Sudeste", "Centro-Oeste"],
        rotulos_colunas=["Aderiu", "Abandonou"],
        conclusao=(
            "χ² calculado ≈ 27,64 >> χ² crítico ≈ 9,49. "
            "REJEITAMOS H₀. A adesão não é homogênea: Norte e Centro-Oeste "
            "apresentam taxas de abandono proporcionalmente maiores que Sul e Sudeste, "
            "indicando necessidade de políticas regionais específicas de saúde."
        ),
    ),

    ExemploContingencia(
        id="modal_transporte_cidades",
        titulo="Modal de Transporte ao Trabalho em 5 Capitais Brasileiras",
        fonte="Cotidiano Brasileiro — Transporte",
        contexto=(
            "O IBGE realizou uma pesquisa sobre mobilidade urbana entrevistando "
            "trabalhadores em cinco capitais brasileiras: São Paulo, Rio de Janeiro, "
            "Belo Horizonte, Fortaleza e Porto Alegre. Cada entrevistado indicou "
            "seu principal meio de transporte ao trabalho. "
            "Queremos verificar se a distribuição entre os modais é homogênea "
            "entre as cidades ou se cada cidade tem um perfil distinto."
        ),
        h0="A distribuição de modais de transporte é IGUAL nas 5 capitais.",
        h1="Pelo menos uma capital tem distribuição de modais DIFERENTE das demais.",
        alpha=0.05,
        tabela=[
            [320, 210, 180, 90],
            [198, 245, 120, 37],
            [112, 198, 143, 47],
            [ 87, 134, 198, 31],
            [143, 167,  89, 101],
        ],
        rotulos_linhas=["São Paulo", "Rio de Janeiro", "Belo Horizonte",
                        "Fortaleza", "Porto Alegre"],
        rotulos_colunas=["Metrô / Ônibus", "Carro", "Moto", "Bicicleta"],
        conclusao=(
            "χ² calculado ≈ 228,83 >> χ² crítico ≈ 21,03. "
            "REJEITAMOS H₀. Cada cidade tem perfil bem distinto: "
            "Fortaleza lidera no uso de moto, Porto Alegre tem maior proporção "
            "de ciclistas, e São Paulo depende mais de transporte coletivo."
        ),
    ),

    ExemploContingencia(
        id="delivery_faixa_etaria",
        titulo="Preferência de Aplicativo de Delivery por Faixa Etária",
        fonte="Cotidiano Brasileiro — Consumo",
        contexto=(
            "Uma consultoria de mercado entrevistou 800 consumidores divididos "
            "em quatro faixas etárias e perguntou qual plataforma de entrega "
            "de alimentos preferem: iFood, Rappi ou compra direta no mercado. "
            "A questão é: diferentes gerações têm o mesmo comportamento de "
            "consumo de delivery, ou cada faixa etária tem um perfil próprio?"
        ),
        h0="A preferência de plataforma de delivery é IGUAL nas quatro faixas etárias.",
        h1="A preferência DIFERE entre pelo menos duas faixas etárias.",
        alpha=0.05,
        tabela=[
            [ 87, 23,  40],
            [102, 41,  57],
            [ 78, 29,  93],
            [ 34, 12, 154],
        ],
        rotulos_linhas=["18 a 24 anos", "25 a 34 anos", "35 a 49 anos", "50 anos ou mais"],
        rotulos_colunas=["iFood", "Rappi", "Mercado / Direto"],
        conclusao=(
            "χ² calculado ≈ 127,44 >> χ² crítico ≈ 12,59. "
            "REJEITAMOS H₀. O perfil é muito diferente por geração: "
            "jovens (18-34) dominam os apps de delivery, enquanto a faixa 50+ "
            "prefere compra direta no mercado — as proporções são claramente heterogêneas."
        ),
    ),
]
