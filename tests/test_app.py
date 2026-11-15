from app.db import get_db


def test_index_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Gestão de Manejo Arbóreo" in response.get_data(as_text=True)


def test_cadastro_valido_persiste_solicitacao(app, client):
    response = client.post(
        "/solicitacoes/nova",
        data={
            "tipo": "Poda de formação",
            "local_referencia": "Praça Exemplo, setor A",
            "prioridade": "Normal",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "registrada" in response.get_data(as_text=True)
    with app.app_context():
        registro = get_db().execute("SELECT * FROM solicitacao").fetchone()
        assert registro["tipo"] == "Poda de formação"
        assert registro["status"] == "Recebida"


def test_cadastro_invalido_exibe_erros_e_nao_persiste(app, client):
    response = client.post(
        "/solicitacoes/nova",
        data={"tipo": "Tipo inexistente", "local_referencia": "x", "prioridade": "Urgente"},
    )

    conteudo = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "tipo de manejo válido" in conteudo
    assert "entre 5 e 120 caracteres" in conteudo
    assert "prioridade válida" in conteudo
    with app.app_context():
        total = get_db().execute("SELECT COUNT(*) FROM solicitacao").fetchone()[0]
        assert total == 0


def test_consulta_filtra_por_protocolo_e_prioridade(client, solicitacao_id):
    response = client.get("/solicitacoes?busca=TESTE-001&prioridade=Alta")
    conteudo = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "DEMO-TESTE-001" in conteudo
    assert "1</strong> resultado" in conteudo


def test_atualizacao_registra_historico(app, client, solicitacao_id):
    response = client.post(
        f"/solicitacoes/{solicitacao_id}",
        data={"status": "Em análise", "observacao": "Triagem demonstrativa concluída."},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Status atualizado" in response.get_data(as_text=True)
    with app.app_context():
        db = get_db()
        solicitacao = db.execute(
            "SELECT status FROM solicitacao WHERE id = ?", (solicitacao_id,)
        ).fetchone()
        historico = db.execute(
            "SELECT * FROM historico_status WHERE solicitacao_id = ?", (solicitacao_id,)
        ).fetchone()
        assert solicitacao["status"] == "Em análise"
        assert historico["status_anterior"] == "Recebida"
        assert historico["status_novo"] == "Em análise"
