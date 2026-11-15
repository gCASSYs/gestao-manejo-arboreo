from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from .db import get_db

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    registros = get_db().execute(
        "SELECT * FROM solicitacao ORDER BY criado_em DESC LIMIT 5"
    ).fetchall()
    return render_template("index.html", registros=registros)


@bp.route("/solicitacoes/nova", methods=("GET", "POST"))
def nova_solicitacao():
    if request.method == "POST":
        tipo = request.form.get("tipo", "").strip()
        local = request.form.get("local_referencia", "").strip()
        prioridade = request.form.get("prioridade", "Normal").strip()

        if not tipo or not local:
            flash("Preencha os campos obrigatórios.", "danger")
        else:
            protocolo = f"DEMO-{datetime.now():%Y%m%d%H%M%S}"
            db = get_db()
            db.execute(
                "INSERT INTO solicitacao (protocolo, tipo, local_referencia, prioridade) VALUES (?, ?, ?, ?)",
                (protocolo, tipo, local, prioridade),
            )
            db.commit()
            flash(f"Solicitação fictícia {protocolo} registrada.", "success")
            return redirect(url_for("main.index"))

    return render_template("nova_solicitacao.html")
