import re


TIPOS_VALIDOS = ("Poda de formação", "Vistoria preventiva", "Remoção autorizada")
PRIORIDADES_VALIDAS = ("Normal", "Alta")
STATUS_VALIDOS = ("Recebida", "Em análise", "Concluída")

CARACTERES_DE_CONTROLE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def normalizar_texto(valor):
    return " ".join((valor or "").strip().split())


def validar_solicitacao(tipo, local, prioridade):
    erros = []
    if tipo not in TIPOS_VALIDOS:
        erros.append("Selecione um tipo de manejo válido.")
    if not local:
        erros.append("Informe um local de referência fictício.")
    elif len(local) < 5 or len(local) > 120:
        erros.append("O local de referência deve ter entre 5 e 120 caracteres.")
    elif CARACTERES_DE_CONTROLE.search(local):
        erros.append("O local de referência contém caracteres não permitidos.")
    if prioridade not in PRIORIDADES_VALIDAS:
        erros.append("Selecione uma prioridade válida.")
    return erros


def validar_atualizacao_status(status_atual, novo_status, observacao):
    if novo_status not in STATUS_VALIDOS:
        return "Selecione um status válido."
    if len(observacao) > 250:
        return "A observação deve ter no máximo 250 caracteres."
    if CARACTERES_DE_CONTROLE.search(observacao):
        return "A observação contém caracteres não permitidos."
    if novo_status == status_atual:
        return "O status informado já está ativo."
    return None
