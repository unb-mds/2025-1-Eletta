import pytest
from unittest.mock import Mock, patch, call, MagicMock
import threading
import socket
import itertools
from servidor.servidor import (
    mandar_mensagem,
    mostrar_resultados,
    virar_host,
    receber_votantes,
    receber_votos,
)


@pytest.fixture
def banco_mock():
    banco = Mock()
    banco.dados = {
        "votantes": {
            "192.168.0.10": {"PORT": 12345},
            "192.168.0.11": {"PORT": 12346},
        },
        "pautas": {
            "Educação": {
                "qtd de votos a favor": 3,
                "qtd de votos contra": 1,
                "qtd de votos anulados": 1,
            }
        },
    }
    return banco


@pytest.fixture
def socket_mock():
    return Mock(spec=socket.socket)


@patch("servidor.servidor.socket.socket")
def test_virar_host_cria_socket_udp(mock_classe_socket):
    mock_instancia_socket = MagicMock()
    mock_classe_socket.return_value = mock_instancia_socket

    servidor = virar_host()

    mock_classe_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_DGRAM)
    mock_instancia_socket.settimeout.assert_called_once_with(1.0)
    mock_instancia_socket.bind.assert_called_once_with(("0.0.0.0", 5555))
    assert servidor == mock_instancia_socket


def test_mandar_mensagem_envia_para_todos(socket_mock, banco_mock):
    mandar_mensagem(banco_mock, socket_mock, "Mensagem de teste")
    chamadas_esperadas = [
        call.sendto(b"Mensagem de teste", (12345, "192.168.0.10")),
        call.sendto(b"Mensagem de teste", (12346, "192.168.0.11")),
    ]
    socket_mock.assert_has_calls(chamadas_esperadas, any_order=True)


def test_mostrar_resultados_envia_resultado_formatado(socket_mock, banco_mock):
    resultado = mostrar_resultados(banco_mock, socket_mock, "Educação")

    assert "Resultado da votação" in resultado
    assert "votos a favor = 60.00%" in resultado
    assert "votos contra = 20.00%" in resultado
    assert "votos nulos = 20.00%" in resultado

    assert socket_mock.sendto.called


def test_receber_votantes(monkeypatch):
    banco_mock = Mock()
    banco_mock.adicionar_votante = Mock()
    banco_mock.serializar_dados = Mock()

    mock_servidor = Mock(spec=socket.socket)

    info_votante = ("192.168.0.100", 54321)
    dado_recebido = b"joined"

    def efeito_colateral_recvfrom(buffer_size):
        if not hasattr(efeito_colateral_recvfrom, "called"):
            efeito_colateral_recvfrom.called = True
            return (dado_recebido, info_votante)
        else:
            raise socket.timeout

    mock_servidor.recvfrom.side_effect = efeito_colateral_recvfrom

    evento_parar = threading.Event()

    def executar_funcao():
        receber_votantes(banco_mock, mock_servidor, evento_parar)

    thread = threading.Thread(target=executar_funcao)
    thread.start()

    import time

    time.sleep(0.1)
    evento_parar.set()

    thread.join(timeout=1)

    banco_mock.adicionar_votante.assert_called_once_with(
        info_votante[1], info_votante[0]
    )
    banco_mock.serializar_dados.assert_called()


def test_receber_votos(monkeypatch):
    banco_mock = Mock()
    banco_mock.registrar_voto = Mock()
    banco_mock.serializar_dados = Mock()

    mock_servidor = Mock(spec=socket.socket)
    voto_json = '["sim", "Educação"]'.encode("utf-8")
    info_votante = ("192.168.0.100", 54321)

    mock_servidor.recvfrom.side_effect = itertools.chain(
        [socket.timeout, (voto_json, info_votante)], itertools.repeat(socket.timeout)
    )

    evento_parar = threading.Event()

    def executar_funcao():
        receber_votos(banco_mock, mock_servidor, evento_parar)

    thread = threading.Thread(target=executar_funcao)
    thread.start()

    import time

    time.sleep(0.1)
    evento_parar.set()
    thread.join(timeout=1)

    assert banco_mock.registrar_voto.call_count == 1
    args, kwargs = banco_mock.registrar_voto.call_args
    assert args[0] == 54321
    assert args[1] == "sim"
    assert args[2] == "Educação"
    banco_mock.serializar_dados.assert_called()
    assert args[2] == "Educação"
    banco_mock.serializar_dados.assert_called()
