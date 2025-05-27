import pytest
from unittest.mock import Mock, patch, call
import threading
import socket
from servidor.servidor import mandar_mensagem, mostrar_resultados


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
