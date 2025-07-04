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


@patch("servidor.servidor.socket.socket")  # Mocka a classe socket.socket
def test_virar_host_cria_socket_udp(mock_socket_class):
    mock_socket_instance = MagicMock()
    mock_socket_class.return_value = mock_socket_instance

    # Chama a função que queremos testar
    server = virar_host()

    # Verificações com asserts simples, padrão pytest
    mock_socket_class.assert_called_once_with(socket.AF_INET, socket.SOCK_DGRAM)
    mock_socket_instance.settimeout.assert_called_once_with(1.0)
    mock_socket_instance.bind.assert_called_once_with(("0.0.0.0", 5555))
    assert server == mock_socket_instance


def test_mandar_mensagem_envia_para_todos(socket_mock, banco_mock):
    mandar_mensagem(banco_mock, socket_mock, "Mensagem de teste")
    expected_calls = [
        call.sendto(b"Mensagem de teste", (12345, "192.168.0.10")),
        call.sendto(b"Mensagem de teste", (12346, "192.168.0.11")),
    ]
    socket_mock.assert_has_calls(expected_calls, any_order=True)


def test_mostrar_resultados_envia_resultado_formatado(socket_mock, banco_mock):
    resultado = mostrar_resultados(banco_mock, socket_mock, "Educação")

    assert "Resultado da votação" in resultado
    assert "votos a favor = 60.00%" in resultado
    assert "votos contra = 20.00%" in resultado
    assert "votos nulos = 20.00%" in resultado

    # Verifica se a função manda mensagem para os votantes
    assert socket_mock.sendto.called


def test_receber_votantes(monkeypatch):
    # Mocks
    banco_mock = Mock()
    banco_mock.adicionar_votante = Mock()
    banco_mock.serializar_dados = Mock()

    # Criar um mock para socket
    server_mock = Mock(spec=socket.socket)

    # Criar dados para retornar do recvfrom
    votante_info = ("192.168.0.100", 54321)
    dado_recebido = b"joined"

    # Criar lista de dados que o recvfrom vai retornar
    # Primeiro retorno válido, depois timeout para parar o loop
    def recvfrom_side_effect(buffer_size):
        if not hasattr(recvfrom_side_effect, "called"):
            recvfrom_side_effect.called = True
            return (dado_recebido, votante_info)
        else:
            raise socket.timeout

    server_mock.recvfrom.side_effect = recvfrom_side_effect

    # Criar o evento que vai parar a função após um ciclo
    parar_event = threading.Event()

    # Rodar receber_votantes em thread para não travar o teste
    def run_func():
        receber_votantes(banco_mock, server_mock, parar_event)

    thread = threading.Thread(target=run_func)
    thread.start()

    # Esperar um pouco para função rodar e depois parar o loop
    import time

    time.sleep(0.1)
    parar_event.set()

    # Espera a thread terminar
    thread.join(timeout=1)

    # Verificar se o banco foi atualizado com os dados corretos
    banco_mock.adicionar_votante.assert_called_once_with(
        votante_info[1], votante_info[0]
    )
    banco_mock.serializar_dados.assert_called()


def test_receber_votos(monkeypatch):
    banco_mock = Mock()
    banco_mock.registrar_voto = Mock()
    banco_mock.serializar_dados = Mock()

    server_mock = Mock(spec=socket.socket)
    voto_json = '["sim", "Educação"]'.encode("utf-8")
    votante_info = ("192.168.0.100", 54321)

    server_mock.recvfrom.side_effect = itertools.chain(
        [socket.timeout, (voto_json, votante_info)], itertools.repeat(socket.timeout)
    )

    parar_event = threading.Event()

    def run_func():
        receber_votos(banco_mock, server_mock, parar_event)

    thread = threading.Thread(target=run_func)
    thread.start()

    import time

    time.sleep(0.1)
    parar_event.set()
    thread.join(timeout=1)

    assert banco_mock.registrar_voto.call_count == 1
    args, kwargs = banco_mock.registrar_voto.call_args
    assert args[0] == 54321  # porta
    assert args[1] == "sim"
    assert args[2] == "Educação"
    banco_mock.serializar_dados.assert_called()
    assert args[2] == "Educação"
    banco_mock.serializar_dados.assert_called()
