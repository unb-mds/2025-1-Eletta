from unittest.mock import patch, MagicMock
from servidor.cliente import (
    virar_votante,
    receber_mensagem,
    votar,
)  # seu arquivo cliente.py


@patch("socket.socket")
def test_virar_votante(mock_socket_class):
    mock_socket = MagicMock()
    mock_socket_class.return_value = mock_socket

    votante = virar_votante()

    # Verifica se socket foi criado e message "joined" foi enviado para o server_addr
    mock_socket.sendto.assert_called_once_with(b"joined", ("127.0.0.1", 5555))
    assert votante == mock_socket


@patch("socket.socket")
def test_receber_mensagem(mock_socket_class):
    mock_socket = MagicMock()
    # Mockar o retorno do recvfrom para simular a mensagem recebida
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

    # Verifica se o voto foi enviado no formato esperado
    mock_socket.sendto.assert_called_once_with(
        b'["sim", "pauta1"]', ("127.0.0.1", 5555)
    )
