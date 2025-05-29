import socket

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
    voto = voto + ", " + pauta
    votante.sendto(voto.encode(), server_addr)


# ------- código para teste -------
# if __name__ == '__main__':
#     votante = virar_votante()
#     pauta = receber_mensagem(votante)
#     while pauta != 'votação encerrada':
#         print(f'pauta em votação = {pauta}')
#         opcao = int(input('escolha uma das opções abaixo\n1 - a favor\n2 - contra\n3 - se abster\nopção = '))
#         if opcao == 1:
#             votar(votante, 'a favor', pauta)
#         elif opcao == 2:
#             votar(votante, 'contra', pauta)
#         elif opcao == 3:
#             votar(votante, 'se abster', pauta)

#         resultado = receber_mensagem(votante)
#         print(resultado)
#         pauta = receber_mensagem(votante)
#     print('votação encerrada')
#     exit()
