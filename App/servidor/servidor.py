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
    """
    Tenta criar o socket do host na porta 5555.
    Retorna o socket em caso de sucesso.
    Retorna None se a porta já estiver em uso (indicando que um host já existe).
    """
    BIND_IP = "0.0.0.0"
    UDP_PORT = 5555
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.settimeout(1.0)

    try:
        # Tenta se vincular à porta
        server.bind((BIND_IP, UDP_PORT))
        print(f"Servidor UDP ativo na porta {UDP_PORT}")
        return server
    except OSError:
        # Este erro ocorre se a porta já estiver ocupada
        print(
            f"Falha ao vincular à porta {UDP_PORT}. Provavelmente já existe um host na rede."
        )
        return None


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
            mensagem = dado.decode()
            ip = votante[0]
            porta = votante[1]

            # Verifica se é uma mensagem de verificação de host
            if mensagem == "host_check":
                # Responde para confirmar que o host está ativo
                server.sendto("host_active".encode(), votante)

                continue
            elif mensagem == "joined":
                # A porta do votante é usada como ID e o IP é armazenado.
                banco_de_dados.adicionar_votante(porta, ip)
                # o ip e a porta estão invertidos para testes
                print(f"votante adicionado ip = {ip}, porta = {porta}")
                banco_de_dados.serializar_dados()
            else:
                print(f"Mensagem desconhecida recebida: {mensagem}")

        except socket.timeout:
            continue
    print("votantes definidos")


# inicia um processo que aguarda por votos até que a flag Parar seja ativada
def receber_votos(
    banco_de_dados: Banco_de_Dados, server: socket.socket, Parar: threading.Event
) -> None:
    # Antes de começar a ouvir os votos, vamos limpar qualquer mensagem antiga.
    print("Limpando buffer de mensagens antigas...")
    while True:
        try:
            # Tenta ler qualquer dado que esteja no buffer. O timeout de 1s já está configurado.
            server.recvfrom(1024)
        except socket.timeout:
            # Se der timeout, significa que o buffer está limpo.
            print("Buffer limpo. Pronto para receber votos.")
            break  # Sai do loop de limpeza
    print("Aguardando votos...")
    while not Parar.is_set():
        try:
            dado, votante = server.recvfrom(1000)
            # Tenta processar a mensagem como um voto em JSON.
            # Se não conseguir, ignora a mensagem e continua o loop.
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
                # Se a mensagem não for um JSON válido ou não tiver o formato esperado,
                # apenas imprime um aviso e continua, sem quebrar.
                print(
                    f"Mensagem inválida ou não-JSON recebida de {votante}. Ignorando."
                )
                continue

        except socket.timeout:
            continue


# computa os resultados e envia-os para todos votantes
def mostrar_resultados(
    banco_de_dados: Banco_de_Dados,
    server: socket.socket,
    pauta: str,
    enviar: bool = True,
) -> str:
    qtd_a_favor = banco_de_dados.dados["pautas"][pauta]["qtd de votos a favor"]
    qtd_contra = banco_de_dados.dados["pautas"][pauta]["qtd de votos contra"]
    qtd_abstencao = banco_de_dados.dados["pautas"][pauta]["qtd de votos anulados"]

    # Monta a string simples com os números separados por espaço
    resultado = f"{qtd_a_favor} {qtd_contra} {qtd_abstencao}"
    # Envia a mensagem apenas se 'enviar' for True
    if enviar:
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
