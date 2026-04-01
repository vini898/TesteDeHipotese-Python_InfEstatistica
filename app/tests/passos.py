"""
Motor de explicação passo a passo.
Gera os 6 passos do método, em linguagem natural,
para cada tipo de teste qui-quadrado.
"""

from dataclasses import dataclass


@dataclass
class Passo:
    numero: int
    titulo: str
    conteudo: str          # HTML simples permitido (negrito, código)
    destaque: str = ""     # valor/fórmula que merece destaque visual


# ─────────────────────────────────────────────────────────────
# ADERÊNCIA
# ─────────────────────────────────────────────────────────────

def passos_aderencia(resultado, tipo_esperada: str) -> list[Passo]:
    dist = "uniforme (E = n / k)" if tipo_esperada == "uniforme" \
           else "personalizada (E = n × p)"
    return [
        Passo(
            numero=1,
            titulo="Escolha do teste estatístico",
            conteudo=(
                "O objetivo é verificar se a distribuição de frequências "
                "observadas se ajusta a uma distribuição teórica. "
                "O teste adequado é o <strong>Qui-Quadrado de Aderência</strong>."
            ),
            destaque="χ² = Σ (O − E)² / E",
        ),
        Passo(
            numero=2,
            titulo="Hipóteses",
            conteudo=(
                "<strong>H₀:</strong> as frequências observadas concordam com a distribuição alegada.<br>"
                "<strong>H₁:</strong> as frequências observadas <em>não</em> concordam com a distribuição alegada."
            ),
        ),
        Passo(
            numero=3,
            titulo="Nível de significância",
            conteudo=(
                f"O nível de significância fixado é <strong>α = {resultado.alpha}</strong>. "
                f"Isso significa que aceitamos, no máximo, {int(resultado.alpha*100)}% de chance "
                "de rejeitar H₀ quando ela for verdadeira (Erro Tipo I)."
            ),
            destaque=f"α = {resultado.alpha}",
        ),
        Passo(
            numero=4,
            titulo="Cálculo da estatística de teste",
            conteudo=(
                f"A amostra tem <strong>n = {resultado.n}</strong> observações "
                f"em <strong>k = {resultado.k}</strong> categorias. "
                f"Distribuição esperada: {dist}.<br>"
                f"Calculando <strong>(O − E)² / E</strong> para cada categoria e somando: "
                f"<span style='white-space:nowrap'>χ² = {resultado.qui2_calculado}.</span>"
            ),
            destaque=f"χ²calc = {resultado.qui2_calculado}",
        ),
        Passo(
            numero=5,
            titulo="Região crítica",
            conteudo=(
                f"Com <strong>k − 1 = {resultado.graus_liberdade}</strong> graus de liberdade "
                f"e α = {resultado.alpha}, o valor crítico da tabela qui-quadrado é "
                f"<strong>χ²c = {resultado.qui2_critico}</strong>.<br>"
                f"A hipótese nula é rejeitada se "
                f"<span style='white-space:nowrap'>χ²calc &gt; χ²c.</span>"
            ),
            destaque=f"χ²crítico = {resultado.qui2_critico}",
        ),
        Passo(
            numero=6,
            titulo="Decisão",
            conteudo=_decisao_aderencia(resultado),
            destaque=f"p-valor = {resultado.p_valor}",
        ),
    ]


def _decisao_aderencia(res) -> str:
    sinal = "&gt;" if res.rejeita_h0 else "≤"
    sinal_p = "≤" if res.rejeita_h0 else "&gt;"
    conclusao = (
        "<strong>REJEITAMOS H₀.</strong> "
        "Há evidência estatística de que as frequências observadas "
        "<em>não</em> seguem a distribuição alegada."
    ) if res.rejeita_h0 else (
        "<strong>NÃO REJEITAMOS H₀.</strong> "
        "Não há evidência suficiente para afirmar que as frequências "
        "diferem da distribuição alegada."
    )
    return (
        f"<span style='white-space:nowrap'>χ²calc = <strong>{res.qui2_calculado}</strong> "
        f"{sinal} χ²c = <strong>{res.qui2_critico}</strong></span> → "
        f"<span style='white-space:nowrap'>p-valor = <strong>{res.p_valor}</strong> "
        f"{sinal_p} α = {res.alpha}</span>.<br>"
        f"{conclusao}"
    )


# ─────────────────────────────────────────────────────────────
# INDEPENDÊNCIA
# ─────────────────────────────────────────────────────────────

def passos_independencia(resultado) -> list[Passo]:
    r, c = resultado.n_linhas, resultado.n_colunas
    return [
        Passo(
            numero=1,
            titulo="Escolha do teste estatístico",
            conteudo=(
                "Os dados estão em uma tabela de contingência com duas variáveis categóricas. "
                "O objetivo é verificar se essas variáveis são independentes. "
                "O teste adequado é o <strong>Qui-Quadrado de Independência</strong>."
            ),
            destaque=f"Tabela {r} × {c}",
        ),
        Passo(
            numero=2,
            titulo="Hipóteses",
            conteudo=(
                "<strong>H₀:</strong> as variáveis linha e coluna são <em>independentes</em>.<br>"
                "<strong>H₁:</strong> as variáveis linha e coluna são <em>dependentes</em>."
            ),
        ),
        Passo(
            numero=3,
            titulo="Nível de significância",
            conteudo=(
                f"Nível de significância fixado: <strong>α = {resultado.alpha}</strong>."
            ),
            destaque=f"α = {resultado.alpha}",
        ),
        Passo(
            numero=4,
            titulo="Cálculo da estatística de teste",
            conteudo=(
                "Para cada célula, calcula-se a frequência esperada:<br>"
                "<code>E = (Total da linha × Total da coluna) / Total geral</code><br>"
                f"Total geral: <strong>{resultado.total_geral}</strong>. "
                f"Em seguida, soma-se <strong>(O − E)² / E</strong> para todas as {r*c} células: "
                f"<span style='white-space:nowrap'>χ² = {resultado.qui2_calculado}.</span>"
            ),
            destaque=f"χ²calc = {resultado.qui2_calculado}",
        ),
        Passo(
            numero=5,
            titulo="Região crítica",
            conteudo=(
                f"Graus de liberdade: "
                f"<strong><span style='white-space:nowrap'>(r−1)(c−1) = ({r}−1)×({c}−1) = {resultado.graus_liberdade}</span></strong>.<br>"
                f"Valor crítico: <strong>χ²c = {resultado.qui2_critico}</strong> "
                f"(α = {resultado.alpha}, cauda direita)."
            ),
            destaque=f"GL = {resultado.graus_liberdade}",
        ),
        Passo(
            numero=6,
            titulo="Decisão",
            conteudo=_decisao_contingencia(resultado, "independentes", "dependentes"),
            destaque=f"p-valor = {resultado.p_valor}",
        ),
    ]


# ─────────────────────────────────────────────────────────────
# HOMOGENEIDADE
# ─────────────────────────────────────────────────────────────

def passos_homogeneidade(resultado) -> list[Passo]:
    g, c = resultado.n_grupos, resultado.n_categorias
    return [
        Passo(
            numero=1,
            titulo="Escolha do teste estatístico",
            conteudo=(
                f"Temos <strong>{g} grupos/populações</strong> distintos, cada um com "
                f"<strong>{c} categorias</strong> de resultado. "
                "O objetivo é verificar se as proporções são as mesmas em todos os grupos. "
                "O teste adequado é o <strong>Qui-Quadrado de Homogeneidade</strong>."
            ),
            destaque=f"{g} grupos × {c} categorias",
        ),
        Passo(
            numero=2,
            titulo="Hipóteses",
            conteudo=(
                "<strong>H₀:</strong> as proporções são <em>homogêneas</em> entre todos os grupos.<br>"
                "<strong>H₁:</strong> pelo menos um grupo tem proporção <em>diferente</em> dos demais."
            ),
        ),
        Passo(
            numero=3,
            titulo="Nível de significância",
            conteudo=(
                f"Nível de significância fixado: <strong>α = {resultado.alpha}</strong>."
            ),
            destaque=f"α = {resultado.alpha}",
        ),
        Passo(
            numero=4,
            titulo="Cálculo da estatística de teste",
            conteudo=(
                "A mecânica de cálculo é idêntica ao teste de independência:<br>"
                "<code>E = (Total do grupo × Total da categoria) / Total geral</code><br>"
                f"Total geral: <strong>{resultado.total_geral}</strong>. "
                f"Somando (O − E)² / E para todas as células: "
                f"<span style='white-space:nowrap'>χ² = {resultado.qui2_calculado}.</span>"
            ),
            destaque=f"χ²calc = {resultado.qui2_calculado}",
        ),
        Passo(
            numero=5,
            titulo="Região crítica",
            conteudo=(
                f"Graus de liberdade: "
                f"<strong><span style='white-space:nowrap'>(grupos−1)(cats−1) = ({g}−1)×({c}−1) = {resultado.graus_liberdade}</span></strong>.<br>"
                f"Valor crítico: <strong>χ²c = {resultado.qui2_critico}</strong> "
                f"(α = {resultado.alpha}, cauda direita)."
            ),
            destaque=f"GL = {resultado.graus_liberdade}",
        ),
        Passo(
            numero=6,
            titulo="Decisão",
            conteudo=_decisao_contingencia(resultado, "homogêneas", "diferentes"),
            destaque=f"p-valor = {resultado.p_valor}",
        ),
    ]


# ─────────────────────────────────────────────────────────────
# HELPER COMPARTILHADO
# ─────────────────────────────────────────────────────────────

def _decisao_contingencia(res, palavra_h0: str, palavra_h1: str) -> str:
    sinal = "&gt;" if res.rejeita_h0 else "≤"
    sinal_p = "≤" if res.rejeita_h0 else "&gt;"
    if res.rejeita_h0:
        conclusao = (
            f"<strong>REJEITAMOS H₀.</strong> "
            f"Há evidência estatística de que as proporções <em>não</em> são {palavra_h0}."
        )
    else:
        conclusao = (
            f"<strong>NÃO REJEITAMOS H₀.</strong> "
            f"Não há evidência suficiente para afirmar que as proporções são {palavra_h1}."
        )
    return (
        f"<span style='white-space:nowrap'>χ²calc = <strong>{res.qui2_calculado}</strong> "
        f"{sinal} χ²c = <strong>{res.qui2_critico}</strong></span> → "
        f"<span style='white-space:nowrap'>p-valor = <strong>{res.p_valor}</strong> "
        f"{sinal_p} α = {res.alpha}</span>.<br>"
        f"{conclusao}"
    )
