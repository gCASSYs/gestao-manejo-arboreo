from app import create_app


def test_index_loads(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db")})
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert "Gestão de Manejo Arbóreo" in response.get_data(as_text=True)
