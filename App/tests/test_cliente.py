from unittest.mock import patch, MagicMock
from servidor.cliente import (
    virar_votante,
    receber_mensagem,
    votar,
    get_broadcast_ip,
    verificar_host_ativo,
)


@patch("socket.socket")
def test_get_broadcast_ip(mock_socket_class):
    mock_socket = MagicMock()
    mock_socket.getsockname.return_value = ("192.168.0.104", 12345)
    mock_socket_class.return_value = mock_socket

    ip = get_broadcast_ip()

    mock_socket.connect.assert_called_once_with(("8.8.8.8", 80))
    mock_socket.getsockname.assert_called_once()
    mock_socket.close.assert_called_once()

    assert ip == "192.168.0.255"


@patch("socket.socket")
def test_virar_votante(mock_socket_class):
    mock_socket = MagicMock()
    mock_socket_class.return_value = mock_socket

    votante = virar_votante()

    mock_socket.sendto.assert_called_once_with(b"joined", ("127.0.0.1", 5555))
    assert votante == mock_socket


@patch("socket.socket")
def test_receber_mensagem(mock_socket_class):
    mock_socket = MagicMock()
    mock_socket.recvfrom.return_value = (b"mensagem do servidor", ("127.0.0.1", 5555))
    mock_socket_class.return_value = mock_socket

    votante = mock_socket
    mensagem = receber_mensagem(votante)

    assert mensagem == "mensagem do servidor"


@patch("socket.socket")
def test_votar(mock_socket_class):
    mock_socket = MagicMock()
    mock_socket_class.return_value = mock_socket

    votante = mock_socket
    votar(votante, "sim", "pauta1")

    mock_socket.sendto.assert_called_once_with(
        b'["sim", "pauta1"]', ("127.0.0.1", 5555)
    )


@patch("socket.socket")
def test_verificar_host_ativo_true(mock_socket_class):
    mock_socket = MagicMock()
    mock_socket.recvfrom.return_value = (b"host_active", ("127.0.0.1", 5555))
    mock_socket_class.return_value = mock_socket

    assert verificar_host_ativo() is True


@patch("socket.socket")
def test_verificar_host_ativo_false(mock_socket_class):
    mock_socket = MagicMock()
    mock_socket.recvfrom.side_effect = TimeoutError
    mock_socket_class.return_value = mock_socket

    assert verificar_host_ativo() is False
