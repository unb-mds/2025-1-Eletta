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
    assert votante["votos nulo"] == []
    assert votante["pautas votadas"] == []


def test_adicionar_pauta():
    bd = Banco_de_Dados()
    bd.adicionar_pauta("pauta1")
    assert "pauta1" in bd.dados["pautas"]
    pauta = bd.dados["pautas"]["pauta1"]
    assert pauta["qtd de votos a favor"] == 0
    assert pauta["qtd de votos contra"] == 0
    assert pauta["qtd de votos anulados"] == 0


def test_registrar_voto_a_favor():
    bd = Banco_de_Dados()
    bd.adicionar_votante("user1", 1234)
    bd.adicionar_pauta("pauta1")
    bd.registrar_voto("user1", "a favor", "pauta1")

    pauta = bd.dados["pautas"]["pauta1"]
    votante = bd.dados["votantes"]["user1"]

    assert pauta["qtd de votos a favor"] == 1
    assert "pauta1" in votante["votos a favor"]
    assert "pauta1" in votante["pautas votadas"]


def test_registrar_voto_contra():
    bd = Banco_de_Dados()
    bd.adicionar_votante("user1", 1234)
    bd.adicionar_pauta("pauta1")
    bd.registrar_voto("user1", "contra", "pauta1")

    pauta = bd.dados["pautas"]["pauta1"]
    votante = bd.dados["votantes"]["user1"]

    assert pauta["qtd de votos contra"] == 1
    assert "pauta1" in votante["votos contra"]
    assert "pauta1" in votante["pautas votadas"]


def test_registrar_voto_nulo():
    bd = Banco_de_Dados()
    bd.adicionar_votante("user1", 1234)
    bd.adicionar_pauta("pauta1")
    bd.registrar_voto("user1", "nulo", "pauta1")

    pauta = bd.dados["pautas"]["pauta1"]
    votante = bd.dados["votantes"]["user1"]

    assert pauta["qtd de votos anulados"] == 1
    assert "pauta1" in votante["votos nulo"]
    assert "pauta1" in votante["pautas votadas"]


def test_registrar_voto_votante_inexistente():
    bd = Banco_de_Dados()
    bd.adicionar_pauta("pauta1")
    bd.registrar_voto("user_inexistente", "a favor", "pauta1")
    pauta = bd.dados["pautas"]["pauta1"]
    assert pauta["qtd de votos a favor"] == 0


def test_registrar_voto_pauta_repetida():
    bd = Banco_de_Dados()
    bd.adicionar_votante("user1", 1234)
    bd.adicionar_pauta("pauta1")
    bd.registrar_voto("user1", "a favor", "pauta1")
    bd.registrar_voto("user1", "contra", "pauta1")

    pauta = bd.dados["pautas"]["pauta1"]
    votante = bd.dados["votantes"]["user1"]

    assert pauta["qtd de votos a favor"] == 1
    assert pauta["qtd de votos contra"] == 0
    assert "pauta1" in votante["votos a favor"]
    assert "pauta1" not in votante["votos contra"]


@patch(
    "builtins.open", new_callable=mock_open, read_data='{"votantes": {}, "pautas": {}}'
)
def test_ler_json(mock_file):
    bd = Banco_de_Dados()
    bd.ler_json()
    assert bd.dados == {"votantes": {}, "pautas": {}}
    mock_file.assert_called_once_with("dados.json", "r")


@patch("builtins.open", new_callable=mock_open)
def test_serializar_dados(mock_file):
    bd = Banco_de_Dados()
    bd.adicionar_votante("user1", 1234)
    bd.adicionar_pauta("pauta1")

    bd.serializar_dados()
    mock_file.assert_called_once_with("servidor/Data_Base/dados.json", "w")
    handle = mock_file()
    handle.write.assert_called() 
