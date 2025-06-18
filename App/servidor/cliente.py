import socket
import json

server_addr = ("127.0.0.1", 5555)


def virar_votante() -> socket.socket:
    votante = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = "joined"
    votante.sendto(message.encode(), server_addr)
    return votante


def receber_mensagem(votante: socket.socket) -> str:
    dados, server = votante.recvfrom(1024)
    mensagem = dados.decode()
    return mensagem


def votar(votante: socket.socket, voto: str, pauta: str) -> None:
    dados = [voto, pauta]
    voto = json.dumps(dados)
    votante.sendto(voto.encode(), server_addr)
