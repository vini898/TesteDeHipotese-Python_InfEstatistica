"""
Motor de interpretação em linguagem natural.
Gera uma conclusão contextualizada baseada no resultado do teste
e, quando disponível, no contexto do exemplo do PDF.
"""


def interpretar_aderencia(resultado, titulo_exemplo: str = "") -> str:
    """Gera parágrafo de interpretação para teste de aderência."""
    nivel = _nivel_evidencia(resultado.p_valor)
    contexto = f' no contexto de "{titulo_exemplo}"' if titulo_exemplo else ""

    if resultado.rejeita_h0:
        return (
            f"Com {int((1 - resultado.alpha) * 100)}% de confiança{contexto}, "
            f"os dados fornecem <strong>{nivel}</strong> de que as frequências observadas "
            f"<em>não seguem</em> a distribuição alegada. "
            f"O χ² calculado ({resultado.qui2_calculado}) é muito superior ao valor crítico "
            f"({resultado.qui2_critico}), e o p-valor ({resultado.p_valor}) "
            f"{'praticamente nulo indica' if resultado.p_valor < 0.001 else 'indica'} "
            f"que uma diferença tão grande entre O e E dificilmente ocorreria por acaso."
        )
    return (
        f"Com {int((1 - resultado.alpha) * 100)}% de confiança{contexto}, "
        f"não há evidência suficiente para rejeitar a distribuição alegada. "
        f"O χ² calculado ({resultado.qui2_calculado}) ficou abaixo do valor crítico "
        f"({resultado.qui2_critico}), e o p-valor ({resultado.p_valor}) indica que "
        f"as diferenças entre O e E podem ser explicadas pela variação amostral."
    )


def interpretar_independencia(resultado, titulo_exemplo: str = "") -> str:
    """Gera parágrafo de interpretação para teste de independência."""
    nivel = _nivel_evidencia(resultado.p_valor)
    contexto = f' para "{titulo_exemplo}"' if titulo_exemplo else ""

    if resultado.rejeita_h0:
        return (
            f"Com {int((1 - resultado.alpha) * 100)}% de confiança{contexto}, "
            f"há <strong>{nivel}</strong> de que as duas variáveis são "
            f"<em>dependentes entre si</em>. "
            f"χ²calc = {resultado.qui2_calculado} &gt; χ²c = {resultado.qui2_critico} "
            f"(p = {resultado.p_valor}). "
            f"Isso significa que conhecer a categoria de uma variável fornece informação "
            f"sobre a distribuição da outra — elas não são independentes."
        )
    return (
        f"Com {int((1 - resultado.alpha) * 100)}% de confiança{contexto}, "
        f"não há evidência suficiente de dependência entre as duas variáveis. "
        f"χ²calc = {resultado.qui2_calculado} ≤ χ²c = {resultado.qui2_critico} "
        f"(p = {resultado.p_valor}). "
        f"As diferenças observadas entre as frequências esperadas e observadas "
        f"são compatíveis com a variação aleatória de uma amostra."
    )


def interpretar_homogeneidade(resultado, titulo_exemplo: str = "") -> str:
    """Gera parágrafo de interpretação para teste de homogeneidade."""
    nivel = _nivel_evidencia(resultado.p_valor)
    contexto = f' para "{titulo_exemplo}"' if titulo_exemplo else ""

    if resultado.rejeita_h0:
        return (
            f"Com {int((1 - resultado.alpha) * 100)}% de confiança{contexto}, "
            f"há <strong>{nivel}</strong> de que as proporções "
            f"<em>diferem significativamente</em> entre os {resultado.n_grupos} grupos. "
            f"χ²calc = {resultado.qui2_calculado} &gt; χ²c = {resultado.qui2_critico} "
            f"(p = {resultado.p_valor}). "
            f"Os grupos não são homogêneos: ao menos uma população apresenta proporções "
            f"distintas das demais."
        )
    return (
        f"Com {int((1 - resultado.alpha) * 100)}% de confiança{contexto}, "
        f"não há evidência de que as proporções difiram entre os {resultado.n_grupos} grupos. "
        f"χ²calc = {resultado.qui2_calculado} ≤ χ²c = {resultado.qui2_critico} "
        f"(p = {resultado.p_valor}). "
        f"As populações podem ser consideradas homogêneas em relação à característica analisada."
    )


# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def _nivel_evidencia(p_valor: float) -> str:
    if p_valor < 0.001:
        return "evidência muito forte"
    if p_valor < 0.01:
        return "evidência forte"
    if p_valor < 0.05:
        return "evidência moderada"
    return "evidência fraca"
