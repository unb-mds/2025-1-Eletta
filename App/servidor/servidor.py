import socket
import threading
from servidor.Data_Base.DB import Banco_de_Dados


def virar_host() -> socket.socket:
    BIND_IP = "0.0.0.0"
    UDP_PORT = 5555
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.settimeout(1.0)
    server.bind((BIND_IP, UDP_PORT))
    print(f"servidor UDP ativo na porta {UDP_PORT}")
    return server


def mandar_mensagem(
    banco_de_dados: Banco_de_Dados, server: socket.socket, mensagem: str
) -> None:
    # Acessa a cópia dos items para evitar problemas com concorrência
    for ip, info in list(banco_de_dados.dados["votantes"].items()):
        porta = info["PORT"]
        # Correção: converte a porta (que está na variável 'ip') para inteiro
        server.sendto(mensagem.encode(), (porta, int(ip)))


def receber_votantes(
    banco_de_dados: Banco_de_Dados, server: socket.socket, Parar: threading.Event
) -> None:
    print("aguardando votantes")
    while not Parar.is_set():
        try:
            dado, votante = server.recvfrom(1000)
            ip = votante[0]
            porta = votante[1]
            banco_de_dados.adicionar_votante(str(porta), ip)  # User ID como string
            print(f"votante adicionado ip = {ip}, porta = {porta}")
            banco_de_dados.serializar_dados()
        except socket.timeout:
            continue
    print("votantes definidos")


def receber_votos(
    banco_de_dados: Banco_de_Dados, server: socket.socket, Parar: threading.Event
) -> None:
    print("recebendo votos")
    while not Parar.is_set():
        try:
            dado, votante = server.recvfrom(1000)
            print("voto recebido")
            dados = dado.decode().split(", ")

            # Adiciona uma verificação para garantir que a mensagem está no formato correto
            if len(dados) >= 2:
                voto = dados[0]
                pauta = dados[1]
                porta = str(votante[1])  # User ID como string
                banco_de_dados.registrar_voto(porta, voto, pauta)
                banco_de_dados.serializar_dados()
            else:
                # Se a mensagem não for um voto, apenas a ignora.
                print(f"Mensagem inesperada (ignorada) de {votante}: {dado.decode()}")

        except socket.timeout:
            continue


def mostrar_resultados(
    banco_de_dados: Banco_de_Dados, server: socket.socket, pauta: str
) -> str:
    resultado = "Resultado da votação:\n\n"
    resultado += f'Pauta: "{pauta}"\n\n'

    pauta_data = banco_de_dados.dados["pautas"].get(pauta, {})
    qtd_a_favor = pauta_data.get("qtd de votos a favor", 0)
    qtd_contra = pauta_data.get("qtd de votos contra", 0)
    qtd_abstenção = pauta_data.get("qtd de votos anulados", 0)

    total = qtd_a_favor + qtd_contra + qtd_abstenção

    if total == 0:
        porcentagem_a_favor = 0.00
        porcentagem_contra = 0.00
        porcentagem_abstenção = 0.00
    else:
        porcentagem_a_favor = (qtd_a_favor / total) * 100
        porcentagem_contra = (qtd_contra / total) * 100
        porcentagem_abstenção = (qtd_abstenção / total) * 100

    resultado += f"Votos a Favor: {qtd_a_favor} ({porcentagem_a_favor:.2f}%)\n"
    resultado += f"Votos Contra: {qtd_contra} ({porcentagem_contra:.2f}%)\n"
    resultado += f"Abstenções: {qtd_abstenção} ({porcentagem_abstenção:.2f}%)\n"
    resultado += f"Total de Votos: {total}"

    mandar_mensagem(banco_de_dados, server, resultado)
    return resultado


def aguardar_votantes(
    server: socket.socket,
) -> tuple[Banco_de_Dados, threading.Thread, threading.Event]:
    Encerrar_espera_por_votantes = threading.Event()
    banco_de_dados = Banco_de_Dados()
    processo = threading.Thread(
        target=receber_votantes,
        args=(banco_de_dados, server, Encerrar_espera_por_votantes),
        daemon=True,
    )
    processo.start()
    return (banco_de_dados, processo, Encerrar_espera_por_votantes)


def aguardar_votos(
    banco_de_dados: Banco_de_Dados, server: socket.socket
) -> tuple[threading.Thread, threading.Event]:
    Encerrar_espera_por_votos = threading.Event()
    processo = threading.Thread(
        target=receber_votos,
        args=(banco_de_dados, server, Encerrar_espera_por_votos),
        daemon=True,
    )
    processo.start()
    return (processo, Encerrar_espera_por_votos)
