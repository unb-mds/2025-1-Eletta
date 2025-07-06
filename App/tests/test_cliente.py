from unittest.mock import patch, MagicMock
from servidor.cliente import (
    virar_votante,
    receber_mensagem,
    votar,
    obter_ip_broadcast,  # Nome atualizado para consistência
    verificar_host_ativo,
)


@patch("socket.socket")
def test_obter_ip_broadcast(mock_classe_socket):
    # Renomeado para refletir a tradução da função original
    socket_mock = MagicMock()
    socket_mock.getsockname.return_value = ("192.168.0.104", 12345)
    mock_classe_socket.return_value = socket_mock

    ip = obter_ip_broadcast()

    socket_mock.connect.assert_called_once_with(("8.8.8.8", 80))
    socket_mock.getsockname.assert_called_once()
    socket_mock.close.assert_called_once()

    assert ip == "192.168.0.255"


@patch("socket.socket")
def test_virar_votante(mock_classe_socket):
    socket_mock = MagicMock()
    mock_classe_socket.return_value = socket_mock

    votante = virar_votante()

    # A mensagem de protocolo "joined" é mantida em inglês
    socket_mock.sendto.assert_called_once_with(b"joined", ("127.0.0.1", 5555))
    assert votante == socket_mock


@patch("socket.socket")
def test_receber_mensagem(mock_classe_socket):
    socket_mock = MagicMock()
    # Mock de uma mensagem recebida do servidor
    socket_mock.recvfrom.return_value = (b"mensagem do servidor", ("127.0.0.1", 5555))
    mock_classe_socket.return_value = socket_mock

    votante = socket_mock
    mensagem = receber_mensagem(votante)

    assert mensagem == "mensagem do servidor"


@patch("socket.socket")
def test_votar(mock_classe_socket):
    socket_mock = MagicMock()
    mock_classe_socket.return_value = socket_mock

    votante = socket_mock
    votar(votante, "sim", "pauta1")

    # Verifica se o voto foi serializado para JSON e enviado corretamente
    socket_mock.sendto.assert_called_once_with(
        b'["sim", "pauta1"]', ("127.0.0.1", 5555)
    )


@patch("socket.socket")
def test_verificar_host_ativo_encontrado(mock_classe_socket):
    # Teste para o caso em que o host é encontrado
    socket_mock = MagicMock()
    # A mensagem de protocolo "host_active" é mantida em inglês
    socket_mock.recvfrom.return_value = (b"host_active", ("127.0.0.1", 5555))
    mock_classe_socket.return_value = socket_mock

    assert verificar_host_ativo() is True


@patch("socket.socket")
def test_verificar_host_ativo_nao_encontrado(mock_classe_socket):
    # Teste para o caso em que o host não responde (timeout)
    socket_mock = MagicMock()
    socket_mock.recvfrom.side_effect = TimeoutError
    mock_classe_socket.return_value = socket_mock

    assert verificar_host_ativo() is False