from app.domain import normalizar_texto, validar_atualizacao_status, validar_solicitacao


def test_normalizar_texto_remove_espacos_excedentes():
    assert normalizar_texto("  Praça   Exemplo  ") == "Praça Exemplo"


def test_validar_solicitacao_rejeita_caractere_de_controle():
    erros = validar_solicitacao("Poda de formação", "Praça\x00Exemplo", "Normal")
    assert "caracteres não permitidos" in erros[0]


def test_validar_atualizacao_status_aceita_transicao():
    assert validar_atualizacao_status("Recebida", "Em análise", "Triagem concluída") is None
