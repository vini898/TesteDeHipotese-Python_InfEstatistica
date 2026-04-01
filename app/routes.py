from flask import Blueprint, render_template, request
from .tests import aderencia, independencia, homogeneidade
from .tests import passos as passos_mod
from .tests import interpretacao as interp_mod
from .tests.exemplos import (
    EXEMPLOS_ADERENCIA,
    EXEMPLOS_INDEPENDENCIA,
    EXEMPLOS_HOMOGENEIDADE,
)

bp = Blueprint("main", __name__)


# ─── HELPERS ─────────────────────────────────────────────────

def _parse_floats(raw: str) -> list[float]:
    raw = raw.replace(",", " ").replace(";", " ")
    return [float(x) for x in raw.split() if x.strip()]


def _parse_matrix(raw: str) -> list[list[float]]:
    rows = []
    for line in raw.strip().splitlines():
        line = line.replace(",", " ").replace(";", " ")
        row = [float(x) for x in line.split() if x.strip()]
        if row:
            rows.append(row)
    return rows


def _matrix_to_text(tabela: list[list[float]]) -> str:
    return "\n".join("  ".join(str(int(v)) for v in row) for row in tabela)


# ─── ÍNDICE ──────────────────────────────────────────────────

@bp.route("/")
def index():
    return render_template("index.html")


# ─── EXEMPLOS ────────────────────────────────────────────────

@bp.route("/exemplos")
def exemplos_view():
    aderencias_resolvidos = []
    for ex in EXEMPLOS_ADERENCIA:
        res = aderencia.executar(ex.observadas, ex.probabilidades, ex.alpha)
        aderencias_resolvidos.append({"exemplo": ex, "resultado": res})

    independencias_resolvidas = []
    for ex in EXEMPLOS_INDEPENDENCIA:
        res = independencia.executar(ex.tabela, ex.alpha)
        independencias_resolvidas.append({"exemplo": ex, "resultado": res})

    homogeneidades_resolvidas = []
    for ex in EXEMPLOS_HOMOGENEIDADE:
        res = homogeneidade.executar(ex.tabela, ex.alpha)
        homogeneidades_resolvidas.append({"exemplo": ex, "resultado": res})

    return render_template(
        "exemplos.html",
        aderencias=aderencias_resolvidos,
        independencias=independencias_resolvidas,
        homogeneidades=homogeneidades_resolvidas,
    )


# ─── ADERÊNCIA ───────────────────────────────────────────────

@bp.route("/aderencia", methods=["GET", "POST"])
def aderencia_view():
    resultado = None
    erro = None
    form = {}
    passos = []
    interpretacao = ""
    titulo_exemplo = ""

    exemplo_id = request.args.get("exemplo")
    if exemplo_id and request.method == "GET":
        ex = next((e for e in EXEMPLOS_ADERENCIA if e.id == exemplo_id), None)
        if ex:
            titulo_exemplo = ex.titulo
            form = {
                "observadas": "  ".join(str(int(v)) for v in ex.observadas),
                "tipo_esperada": "personalizada" if ex.probabilidades else "uniforme",
                "probabilidades": "  ".join(str(p) for p in ex.probabilidades) if ex.probabilidades else "",
                "alpha": str(ex.alpha),
            }
            try:
                resultado = aderencia.executar(ex.observadas, ex.probabilidades, ex.alpha)
                passos = passos_mod.passos_aderencia(resultado, form["tipo_esperada"])
                interpretacao = interp_mod.interpretar_aderencia(resultado, titulo_exemplo)
            except Exception as e:
                erro = str(e)

    elif request.method == "POST":
        form = request.form.to_dict()
        try:
            obs   = _parse_floats(form.get("observadas", ""))
            alpha = float(form.get("alpha", 0.05))
            tipo  = form.get("tipo_esperada", "uniforme")
            probs = None
            if tipo == "personalizada":
                probs = _parse_floats(form.get("probabilidades", ""))
            resultado = aderencia.executar(obs, probs, alpha)
            passos = passos_mod.passos_aderencia(resultado, tipo)
            interpretacao = interp_mod.interpretar_aderencia(resultado)
        except Exception as e:
            erro = str(e)

    return render_template(
        "aderencia.html",
        resultado=resultado, erro=erro, form=form,
        exemplos=EXEMPLOS_ADERENCIA,
        passos=passos, interpretacao=interpretacao,
        titulo_exemplo=titulo_exemplo,
    )


# ─── INDEPENDÊNCIA ───────────────────────────────────────────

@bp.route("/independencia", methods=["GET", "POST"])
def independencia_view():
    resultado = None
    erro = None
    form = {}
    passos = []
    interpretacao = ""
    titulo_exemplo = ""

    exemplo_id = request.args.get("exemplo")
    if exemplo_id and request.method == "GET":
        ex = next((e for e in EXEMPLOS_INDEPENDENCIA if e.id == exemplo_id), None)
        if ex:
            titulo_exemplo = ex.titulo
            form = {"tabela": _matrix_to_text(ex.tabela), "alpha": str(ex.alpha)}
            try:
                resultado = independencia.executar(ex.tabela, ex.alpha)
                passos = passos_mod.passos_independencia(resultado)
                interpretacao = interp_mod.interpretar_independencia(resultado, titulo_exemplo)
            except Exception as e:
                erro = str(e)

    elif request.method == "POST":
        form = request.form.to_dict()
        try:
            tabela = _parse_matrix(form.get("tabela", ""))
            alpha  = float(form.get("alpha", 0.05))
            resultado = independencia.executar(tabela, alpha)
            passos = passos_mod.passos_independencia(resultado)
            interpretacao = interp_mod.interpretar_independencia(resultado)
        except Exception as e:
            erro = str(e)

    return render_template(
        "independencia.html",
        resultado=resultado, erro=erro, form=form,
        exemplos=EXEMPLOS_INDEPENDENCIA,
        passos=passos, interpretacao=interpretacao,
        titulo_exemplo=titulo_exemplo,
    )


# ─── HOMOGENEIDADE ───────────────────────────────────────────

@bp.route("/homogeneidade", methods=["GET", "POST"])
def homogeneidade_view():
    resultado = None
    erro = None
    form = {}
    passos = []
    interpretacao = ""
    titulo_exemplo = ""

    exemplo_id = request.args.get("exemplo")
    if exemplo_id and request.method == "GET":
        ex = next((e for e in EXEMPLOS_HOMOGENEIDADE if e.id == exemplo_id), None)
        if ex:
            titulo_exemplo = ex.titulo
            form = {"tabela": _matrix_to_text(ex.tabela), "alpha": str(ex.alpha)}
            try:
                resultado = homogeneidade.executar(ex.tabela, ex.alpha)
                passos = passos_mod.passos_homogeneidade(resultado)
                interpretacao = interp_mod.interpretar_homogeneidade(resultado, titulo_exemplo)
            except Exception as e:
                erro = str(e)

    elif request.method == "POST":
        form = request.form.to_dict()
        try:
            tabela = _parse_matrix(form.get("tabela", ""))
            alpha  = float(form.get("alpha", 0.05))
            resultado = homogeneidade.executar(tabela, alpha)
            passos = passos_mod.passos_homogeneidade(resultado)
            interpretacao = interp_mod.interpretar_homogeneidade(resultado)
        except Exception as e:
            erro = str(e)

    return render_template(
        "homogeneidade.html",
        resultado=resultado, erro=erro, form=form,
        exemplos=EXEMPLOS_HOMOGENEIDADE,
        passos=passos, interpretacao=interpretacao,
        titulo_exemplo=titulo_exemplo,
    )
