from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from .db import get_db

bp = Blueprint("main", __name__)

TIPOS_VALIDOS = ("Poda de formação", "Vistoria preventiva", "Remoção autorizada")
PRIORIDADES_VALIDAS = ("Normal", "Alta")
STATUS_VALIDOS = ("Recebida", "Em análise", "Concluída")


def validar_solicitacao(tipo, local, prioridade):
    erros = []
    if tipo not in TIPOS_VALIDOS:
        erros.append("Selecione um tipo de manejo válido.")
    if not local:
        erros.append("Informe um local de referência fictício.")
    elif len(local) < 5 or len(local) > 120:
        erros.append("O local de referência deve ter entre 5 e 120 caracteres.")
    if prioridade not in PRIORIDADES_VALIDAS:
        erros.append("Selecione uma prioridade válida.")
    return erros


@bp.get("/")
def index():
    registros = get_db().execute(
        "SELECT * FROM solicitacao ORDER BY criado_em DESC LIMIT 5"
    ).fetchall()
    return render_template("index.html", registros=registros)


@bp.get("/solicitacoes")
def listar_solicitacoes():
    busca = request.args.get("busca", "").strip()
    status = request.args.get("status", "").strip()
    prioridade = request.args.get("prioridade", "").strip()

    consulta = "SELECT * FROM solicitacao WHERE 1 = 1"
    parametros = []
    if busca:
        consulta += " AND (protocolo LIKE ? OR local_referencia LIKE ?)"
        termo = f"%{busca}%"
        parametros.extend((termo, termo))
    if status:
        consulta += " AND status = ?"
        parametros.append(status)
    if prioridade in PRIORIDADES_VALIDAS:
        consulta += " AND prioridade = ?"
        parametros.append(prioridade)
    consulta += " ORDER BY criado_em DESC"

    registros = get_db().execute(consulta, parametros).fetchall()
    return render_template(
        "solicitacoes.html",
        registros=registros,
        busca=busca,
        status=status,
        prioridade=prioridade,
        prioridades=PRIORIDADES_VALIDAS,
    )


@bp.route("/solicitacoes/nova", methods=("GET", "POST"))
def nova_solicitacao():
    if request.method == "POST":
        tipo = request.form.get("tipo", "").strip()
        local = request.form.get("local_referencia", "").strip()
        prioridade = request.form.get("prioridade", "Normal").strip()

        erros = validar_solicitacao(tipo, local, prioridade)
        if erros:
            for erro in erros:
                flash(erro, "danger")
        else:
            protocolo = f"DEMO-{datetime.now():%Y%m%d%H%M%S%f}"
            db = get_db()
            db.execute(
                "INSERT INTO solicitacao (protocolo, tipo, local_referencia, prioridade) VALUES (?, ?, ?, ?)",
                (protocolo, tipo, local, prioridade),
            )
            solicitacao_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
            db.execute(
                "INSERT INTO historico_status (solicitacao_id, status_novo, observacao) VALUES (?, ?, ?)",
                (solicitacao_id, "Recebida", "Solicitação fictícia cadastrada."),
            )
            db.commit()
            flash(f"Solicitação fictícia {protocolo} registrada.", "success")
            return redirect(url_for("main.index"))

    return render_template(
        "nova_solicitacao.html",
        tipos=TIPOS_VALIDOS,
        prioridades=PRIORIDADES_VALIDAS,
    )


@bp.route("/solicitacoes/<int:solicitacao_id>", methods=("GET", "POST"))
def detalhe_solicitacao(solicitacao_id):
    db = get_db()
    solicitacao = db.execute(
        "SELECT * FROM solicitacao WHERE id = ?", (solicitacao_id,)
    ).fetchone()
    if solicitacao is None:
        return render_template("404.html"), 404

    if request.method == "POST":
        novo_status = request.form.get("status", "").strip()
        observacao = request.form.get("observacao", "").strip()
        if novo_status not in STATUS_VALIDOS:
            flash("Selecione um status válido.", "danger")
        elif len(observacao) > 250:
            flash("A observação deve ter no máximo 250 caracteres.", "danger")
        elif novo_status == solicitacao["status"]:
            flash("O status informado já está ativo.", "warning")
        else:
            db.execute(
                "UPDATE solicitacao SET status = ? WHERE id = ?",
                (novo_status, solicitacao_id),
            )
            db.execute(
                "INSERT INTO historico_status (solicitacao_id, status_anterior, status_novo, observacao) VALUES (?, ?, ?, ?)",
                (solicitacao_id, solicitacao["status"], novo_status, observacao),
            )
            db.commit()
            flash("Status atualizado e registrado no histórico.", "success")
            return redirect(url_for("main.detalhe_solicitacao", solicitacao_id=solicitacao_id))

    historico = db.execute(
        "SELECT * FROM historico_status WHERE solicitacao_id = ? ORDER BY criado_em DESC, id DESC",
        (solicitacao_id,),
    ).fetchall()
    return render_template(
        "detalhe_solicitacao.html",
        solicitacao=solicitacao,
        historico=historico,
        status_validos=STATUS_VALIDOS,
    )
