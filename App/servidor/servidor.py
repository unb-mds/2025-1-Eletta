import socket
import threading
from servidor.Data_Base.DB import Banco_de_Dados
import json


# ----- inicialização do servidor -----
def virar_host() -> socket.socket:
    BIND_IP = "0.0.0.0"
    UDP_PORT = 5555
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.settimeout(1.0)
    server.bind((BIND_IP, UDP_PORT))
    print(f"servidor UDP ativo na porta {UDP_PORT}")
    return server


# ----- funções -----


# manda uma mensagem para todos os clientes presente no banco de dados
def mandar_mensagem(
    banco_de_dados: Banco_de_Dados, server: socket.socket, mensagem: str
) -> None:
    for ip, info in banco_de_dados.dados["votantes"].items():
        porta = info["PORT"]
        server.sendto(
            mensagem.encode(), (porta, ip)
        )  # o ip e a porta estão invertidos para testes


# inicia um processo que aguarda por votantes até que a flag Parar seja ativada
def receber_votantes(
    banco_de_dados: Banco_de_Dados, server: socket.socket, Parar: threading.Event
) -> None:
    print("aguardando votantes")
    while not Parar.is_set():
        try:
            dado, votante = server.recvfrom(1000)
            ip = votante[0]
            porta = votante[1]
            # A porta do votante é usada como ID e o IP é armazenado.
            banco_de_dados.adicionar_votante(porta, ip)
            # o ip e a porta estão invertidos para testes
            print(f"votante adicionado ip = {ip}, porta = {porta}")
            banco_de_dados.serializar_dados()
        except socket.timeout:
            continue
    print("votantes definidos")


# inicia um processo que aguarda por votos até que a flag Parar seja ativada
def receber_votos(
    banco_de_dados: Banco_de_Dados, server: socket.socket, Parar: threading.Event
) -> None:
    print("recebendo votos")
    while not Parar.is_set():
        try:
            dado, votante = server.recvfrom(1000)
            print("voto recebido")
            dados = json.loads(dado.decode())
            voto = dados[0]
            pauta = dados[1]
            # ip = votante[0]
            porta = votante[1]
            # O voto é registrado usando a porta do votante como identificador.
            banco_de_dados.registrar_voto(
                porta, voto, pauta
            )  # em vez de porta precisa ser ip, porém estou usando porta para testes
            banco_de_dados.serializar_dados()
        except socket.timeout:
            continue


# computa os resultados e envia-os para todos votantes
def mostrar_resultados(
    banco_de_dados: Banco_de_Dados, server: socket.socket, pauta: str
) -> str:
    resultado = "-----------------Resultado da votação!-----------------\n"
    resultado += f"pauta discutida |{pauta}|\n"
    qtd_a_favor = banco_de_dados.dados["pautas"][pauta]["qtd de votos a favor"]
    qtd_contra = banco_de_dados.dados["pautas"][pauta]["qtd de votos contra"]
    qtd_abstenção = banco_de_dados.dados["pautas"][pauta]["qtd de votos anulados"]
    total = qtd_a_favor + qtd_contra + qtd_abstenção

    # --- Início da Correção ---
    # Verifica se o total de votos é zero para evitar o erro de divisão por zero.
    if total == 0:
        porcentagem_a_favor = 0.0
        porcentagem_contra = 0.0
        porcentagem_abstenção = 0.0
    else:
        # Se houver votos, calcula as porcentagens normalmente.
        porcentagem_a_favor = qtd_a_favor / total * 100
        porcentagem_contra = qtd_contra / total * 100
        porcentagem_abstenção = qtd_abstenção / total * 100
    # --- Fim da Correção ---

    resultado += f"votos a favor = {porcentagem_a_favor:.2f}%\nvotos contra = {porcentagem_contra:.2f}%\nvotos nulos = {porcentagem_abstenção:.2f}%\n"
    resultado += (
        "-------------------------------------------------------------------\n\n"
    )
    mandar_mensagem(banco_de_dados, server, resultado)
    return resultado


# inicia um processo que aguarda por votantes até que a flag Parar seja ativada
def aguardar_votantes(
    server: socket.socket,
) -> tuple[Banco_de_Dados, threading.Thread, threading.Event]:
    Encerrar_espera_por_votantes = (
        threading.Event()
    )  # criação de flag para o processo de esperar votantes
    banco_de_dados = Banco_de_Dados()
    processo = threading.Thread(
        target=receber_votantes,
        args=(banco_de_dados, server, Encerrar_espera_por_votantes),
    )
    processo.start()
    return (banco_de_dados, processo, Encerrar_espera_por_votantes)


def aguardar_votos(
    banco_de_dados: Banco_de_Dados, server: socket.socket
) -> tuple[threading.Thread, threading.Event]:
    Encerrar_espera_por_votos = (
        threading.Event()
    )  # criação de flag para o processo de esperar votos
    processo = threading.Thread(
        target=receber_votos, args=(banco_de_dados, server, Encerrar_espera_por_votos)
    )
    processo.start()
    return (processo, Encerrar_espera_por_votos)
