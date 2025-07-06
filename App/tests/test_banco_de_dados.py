from unittest.mock import mock_open, patch
from servidor.Data_Base.DB import (
    Banco_de_Dados,
)


def test_adicionar_votante():
    bd = Banco_de_Dados()
    bd.adicionar_votante("user1", 1234)
    assert "user1" in bd.dados["votantes"]
    votante = bd.dados["votantes"]["user1"]
    assert votante["PORT"] == 1234
    assert votante["votos a favor"] == []
    assert votante["votos contra"] == []
    assert votante["votos nulos"] == []  # Corrigido para "nulos"
    assert votante["pautas votadas"] == []


def test_adicionar_pauta():
    bd = Banco_de_Dados()
    bd.adicionar_pauta("pauta1")
    assert "pauta1" in bd.dados["pautas"]
    pauta = bd.dados["pautas"]["pauta1"]
    assert pauta["qtd de votos a favor"] == 0
    assert pauta["qtd de votos contra"] == 0
    assert pauta["qtd de votos nulos"] == 0  # Corrigido para "nulos"


def test_registrar_voto_a_favor():
    bd = Banco_de_Dados()
    bd.adicionar_votante("user1", 1234)
    bd.adicionar_pauta("pauta1")
    # O método registrar_voto usa "A favor" com A maiúsculo
    bd.registrar_voto("user1", "A favor", "pauta1")

    pauta = bd.dados["pautas"]["pauta1"]
    votante = bd.dados["votantes"]["user1"]

    assert pauta["qtd de votos a favor"] == 1
    assert "pauta1" in votante["votos a favor"]
    assert "pauta1" in votante["pautas votadas"]


def test_registrar_voto_contra():
    bd = Banco_de_Dados()
    bd.adicionar_votante("user1", 1234)
    bd.adicionar_pauta("pauta1")
    # O método registrar_voto usa "Contra" com C maiúsculo
    bd.registrar_voto("user1", "Contra", "pauta1")

    pauta = bd.dados["pautas"]["pauta1"]
    votante = bd.dados["votantes"]["user1"]

    assert pauta["qtd de votos contra"] == 1
    assert "pauta1" in votante["votos contra"]
    assert "pauta1" in votante["pautas votadas"]


def test_registrar_voto_nulo():
    bd = Banco_de_Dados()
    bd.adicionar_votante("user1", 1234)
    bd.adicionar_pauta("pauta1")
    # O método registrar_voto usa "Abster-se"
    bd.registrar_voto("user1", "Abster-se", "pauta1")

    pauta = bd.dados["pautas"]["pauta1"]
    votante = bd.dados["votantes"]["user1"]

    assert pauta["qtd de votos nulos"] == 1  # Corrigido para "nulos"
    assert "pauta1" in votante["votos nulos"]  # Corrigido para "nulos"
    assert "pauta1" in votante["pautas votadas"]


def test_registrar_voto_votante_inexistente():
    bd = Banco_de_Dados()
    bd.adicionar_pauta("pauta1")
    bd.registrar_voto("user_inexistente", "A favor", "pauta1")
    pauta = bd.dados["pautas"]["pauta1"]
    assert pauta["qtd de votos a favor"] == 0


def test_registrar_voto_pauta_repetida():
    bd = Banco_de_Dados()
    bd.adicionar_votante("user1", 1234)
    bd.adicionar_pauta("pauta1")
    bd.registrar_voto("user1", "A favor", "pauta1")
    bd.registrar_voto("user1", "Contra", "pauta1")  # Segunda tentativa de voto

    pauta = bd.dados["pautas"]["pauta1"]
    votante = bd.dados["votantes"]["user1"]

    # Garante que apenas o primeiro voto foi computado
    assert pauta["qtd de votos a favor"] == 1
    assert pauta["qtd de votos contra"] == 0
    assert "pauta1" in votante["votos a favor"]
    assert "pauta1" not in votante["votos contra"]


@patch(
    "builtins.open", new_callable=mock_open, read_data='{"votantes": {}, "pautas": {}}'
)
def test_ler_json(arquivo_mock):
    bd = Banco_de_Dados()
    bd.ler_json()
    assert bd.dados == {"votantes": {}, "pautas": {}}
    # Corrigido caminho para consistência
    arquivo_mock.assert_called_once_with("servidor/Data_Base/dados.json", "r")


@patch("builtins.open", new_callable=mock_open)
def test_serializar_dados(arquivo_mock):
    bd = Banco_de_Dados()
    bd.adicionar_votante("user1", 1234)
    bd.adicionar_pauta("pauta1")

    bd.serializar_dados()
    arquivo_mock.assert_called_once_with("servidor/Data_Base/dados.json", "w")
    manipulador_arquivo = arquivo_mock()
    manipulador_arquivo.write.assert_called()