import pytest

from app import create_app
from app.db import get_db


@pytest.fixture()
def app(tmp_path):
    return create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-key",
            "DATABASE": str(tmp_path / "test.db"),
        }
    )


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def solicitacao_id(app):
    with app.app_context():
        db = get_db()
        cursor = db.execute(
            "INSERT INTO solicitacao (protocolo, tipo, local_referencia, prioridade) VALUES (?, ?, ?, ?)",
            ("DEMO-TESTE-001", "Vistoria preventiva", "Praça Exemplo, setor B", "Alta"),
        )
        db.commit()
        return cursor.lastrowid
