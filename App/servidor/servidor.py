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


def mandar_mensagem(banco_de_dados: Banco_de_Dados, server: socket.socket, mensagem: str) -> None:
    for ip, info in banco_de_dados.dados["votantes"].items():
        porta = info["PORT"]
        server.sendto(mensagem.encode(), (porta, ip))


def receber_votantes(banco_de_dados: Banco_de_Dados, server: socket.socket, Parar: threading.Event) -> None:
    print("aguardando votantes")
    while not Parar.is_set():
        try:
            dado, votante = server.recvfrom(1000)
            ip = votante[0]
            porta = votante[1]
            banco_de_dados.adicionar_votante(porta, ip)
            print(f"votante adicionado ip = {ip}, porta = {porta}")
            banco_de_dados.serializar_dados()
        except socket.timeout:
            continue
    print("votantes definidos")


def receber_votos(banco_de_dados: Banco_de_Dados, server: socket.socket, Parar: threading.Event) -> None:
    print("recebendo votos")
    while not Parar.is_set():
        try:
            dado, votante = server.recvfrom(1000)
            print("voto recebido")
            dados = dado.decode().split(", ")
            voto = dados[0]
            pauta = dados[1]
            porta = votante[1]
            banco_de_dados.registrar_voto(porta, voto, pauta)
            banco_de_dados.serializar_dados()
        except socket.timeout:
            continue


def mostrar_resultados(banco_de_dados: Banco_de_Dados, server: socket.socket, pauta: str) -> str:
    resultado = "-----------------Resultado da votação!-----------------\n"
    resultado += f"pauta discutida |{pauta}|\n"
    qtd_a_favor = banco_de_dados.dados["pautas"][pauta]["qtd de votos a favor"]
    qtd_contra = banco_de_dados.dados["pautas"][pauta]["qtd de votos contra"]
    qtd_abstenção = banco_de_dados.dados["pautas"][pauta]["qtd de votos anulados"]
    total = qtd_a_favor + qtd_contra + qtd_abstenção

    if total == 0:
        porcentagem_a_favor = 0.00
        porcentagem_contra = 0.00
        porcentagem_abstenção = 0.00
    else:
        porcentagem_a_favor = qtd_a_favor / total * 100
        porcentagem_contra = qtd_contra / total * 100
        porcentagem_abstenção = qtd_abstenção / total * 100

    resultado += (
        f"votos a favor = {porcentagem_a_favor:.2f}%\nvotos contra = {porcentagem_contra:.2f}%\nvotos nulos = {porcentagem_abstenção:.2f}%\n"
    )
    resultado += "-------------------------------------------------------------------\n\n"
    mandar_mensagem(banco_de_dados, server, resultado)
    return resultado


def aguardar_votantes(server: socket.socket) -> (Banco_de_Dados, threading.Thread, threading.Event):
    Encerrar_espera_por_votantes = threading.Event()
    banco_de_dados = Banco_de_Dados()
    processo = threading.Thread(
        target=receber_votantes, args=(banco_de_dados, server, Encerrar_espera_por_votantes)
    )
    processo.start()
    return (banco_de_dados, processo, Encerrar_espera_por_votantes)


def aguardar_votos(banco_de_dados: Banco_de_Dados, server: socket.socket) -> (threading.Thread, threading.Event):
    Encerrar_espera_por_votos = threading.Event()
    processo = threading.Thread(
        target=receber_votos, args=(banco_de_dados, server, Encerrar_espera_por_votos)
    )
    processo.start()
    return (processo, Encerrar_espera_por_votos)


if __name__ == "__main__":
    server = virar_host()
    Encerrar_espera_por_votantes = threading.Event()
    banco_de_dados = Banco_de_Dados()
    processo = threading.Thread(
        target=receber_votantes, args=(banco_de_dados, server, Encerrar_espera_por_votantes)
    )
    processo.start()
    input("Aperte enter para iniciar a votação\n")
    Encerrar_espera_por_votantes.set()
    processo.join()

    opcao = 1
    while opcao == 1:
        pauta = input("Qual será a pauta discutida? ")
        banco_de_dados.adicionar_pauta(pauta)
        banco_de_dados.serializar_dados()
        mandar_mensagem(banco_de_dados, server, pauta)
        Encerrar_periodo_de_voto = threading.Event()
        processo = threading.Thread(
            target=receber_votos, args=(banco_de_dados, server, Encerrar_periodo_de_voto)
        )
        processo.start()
        input("aperte enter para encerrar a votação\n")
        Encerrar_periodo_de_voto.set()
        processo.join()
        mostrar_resultados(banco_de_dados, server, pauta)
        opcao = int(input("digite 1 para levantar outra pauta "))
    mensagem = "votação encerrada"
    mandar_mensagem(banco_de_dados, server, mensagem)
    print(mensagem)