import socket
import threading
from servidor.Data_Base.DB import Banco_de_Dados
import json


def ip_local():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


# ----- inicialização do servidor -----
def virar_host() -> socket.socket | None:
    BIND_IP = "0.0.0.0"
    UDP_PORT = 5555
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.settimeout(1.0)

    try:
        server.bind((BIND_IP, UDP_PORT))
        print(f"Servidor UDP ativo na porta {UDP_PORT}")
        return server
    except OSError:
        print(
            f"Falha ao vincular à porta {UDP_PORT}. Provavelmente já existe um host na rede."
        )
        return None


def mandar_mensagem(
    banco_de_dados: Banco_de_Dados, server: socket.socket, mensagem: str
) -> None:
    for ip, info in banco_de_dados.dados["votantes"].items():
        porta = info["PORT"]
        server.sendto(
            mensagem.encode(), (porta, ip)
        ) 


def receber_votantes(
    banco_de_dados: Banco_de_Dados, server: socket.socket, Parar: threading.Event
) -> None:
    print("aguardando votantes")
    while not Parar.is_set():
        try:
            dado, votante = server.recvfrom(1000)
            mensagem = dado.decode()
            ip = votante[0]
            porta = votante[1]

            if mensagem == "host_check":
                server.sendto("host_active".encode(), votante)

                continue
            elif mensagem == "joined":
                banco_de_dados.adicionar_votante(porta, ip)
                print(f"votante adicionado ip = {ip}, porta = {porta}")
                banco_de_dados.serializar_dados()
            else:
                print(f"Mensagem desconhecida recebida: {mensagem}")

        except socket.timeout:
            continue
    print("votantes definidos")


def receber_votos(
    banco_de_dados: Banco_de_Dados, server: socket.socket, Parar: threading.Event
) -> None:
    print("Limpando buffer de mensagens antigas...")
    while True:
        try:
            server.recvfrom(1024)
        except socket.timeout:
            print("Buffer limpo. Pronto para receber votos.")
            break  
    print("Aguardando votos...")
    while not Parar.is_set():
        try:
            dado, votante = server.recvfrom(1000)
            try:
                print("voto recebido, tentando decodificar...")
                dados = json.loads(dado.decode())
                voto = dados[0]
                pauta = dados[1]
                porta = votante[1]

                banco_de_dados.registrar_voto(porta, voto, pauta)
                banco_de_dados.serializar_dados()
                print("Voto registrado com sucesso!")

            except (json.JSONDecodeError, IndexError):
                print(
                    f"Mensagem inválida ou não-JSON recebida de {votante}. Ignorando."
                )
                continue

        except socket.timeout:
            continue


def mostrar_resultados(
    banco_de_dados: Banco_de_Dados,
    server: socket.socket,
    pauta: str,
    enviar: bool = True,
) -> str:
    resultado = "-----------------Resultado da votação!-----------------\n"
    resultado += f"pauta discutida |{pauta}|\n"
    qtd_a_favor = banco_de_dados.dados["pautas"][pauta]["qtd de votos a favor"]
    qtd_contra = banco_de_dados.dados["pautas"][pauta]["qtd de votos contra"]
    qtd_abstenção = banco_de_dados.dados["pautas"][pauta]["qtd de votos anulados"]
    total = qtd_a_favor + qtd_contra + qtd_abstenção

    if total == 0:
        porcentagem_a_favor = 0.0
        porcentagem_contra = 0.0
        porcentagem_abstenção = 0.0
    else:
        porcentagem_a_favor = qtd_a_favor / total * 100
        porcentagem_contra = qtd_contra / total * 100
        porcentagem_abstenção = qtd_abstenção / total * 100

    resultado += f"votos a favor = {porcentagem_a_favor:.2f}%\nvotos contra = {porcentagem_contra:.2f}%\nvotos nulos = {porcentagem_abstenção:.2f}%\n"
    resultado += (
        "-------------------------------------------------------------------\n\n"
    )

    if enviar:
        mandar_mensagem(banco_de_dados, server, resultado)

    return resultado


def aguardar_votantes(
    server: socket.socket,
) -> tuple[Banco_de_Dados, threading.Thread, threading.Event]:
    Encerrar_espera_por_votantes = (
        threading.Event()
    )  
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
    ) 
    processo = threading.Thread(
        target=receber_votos, args=(banco_de_dados, server, Encerrar_espera_por_votos)
    )
    processo.start()
    return (processo, Encerrar_espera_por_votos)
