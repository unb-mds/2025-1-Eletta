import socket
import threading
from servidor.Data_Base.DB import Banco_de_Dados
import json


def ip_local():
    """Obtém o endereço de IP local da máquina."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


# ----- Inicialização do servidor -----
def virar_host() -> socket.socket | None:
    """Cria e vincula o socket do servidor (host) para escutar na rede."""
    IP_VINCULADO = "0.0.0.0"  # Escuta em todas as interfaces de rede
    PORTA_UDP = 5555
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.settimeout(1.0)

    try:
        servidor.bind((IP_VINCULADO, PORTA_UDP))
        print(f"Servidor UDP ativo na porta {PORTA_UDP}")
        return servidor
    except OSError:
        print(
            f"Falha ao vincular à porta {PORTA_UDP}. Provavelmente já existe um host na rede."
        )
        return None


def mandar_mensagem(
    banco_de_dados: Banco_de_Dados, servidor: socket.socket, mensagem: str
) -> None:
    """Envia uma mensagem para todos os votantes registrados no banco de dados."""
    for ip, informacoes in banco_de_dados.dados["votantes"].items():
        porta = informacoes["PORT"]
        servidor.sendto(
            mensagem.encode(), (ip, porta)
        )


def receber_votantes(
    banco_de_dados: Banco_de_Dados, servidor: socket.socket, evento_parar: threading.Event
) -> None:
    """Laço de repetição para descobrir e adicionar novos votantes."""
    print("Aguardando votantes...")
    while not evento_parar.is_set():
        try:
            dado, votante = servidor.recvfrom(1000)
            mensagem = dado.decode()
            ip = votante[0]
            porta = votante[1]

            # Responde a verificações de host ativo pela rede
            if mensagem == "host_check":
                servidor.sendto("host_active".encode(), votante)
                continue
            # Adiciona um novo votante que entrou na sessão
            elif mensagem == "joined":
                banco_de_dados.adicionar_votante(porta, ip)
                print(f"Votante adicionado: IP = {ip}, Porta = {porta}")
                banco_de_dados.serializar_dados()
            else:
                print(f"Mensagem desconhecida recebida: {mensagem}")

        except socket.timeout:
            continue
    print("Espera por votantes encerrada.")


def receber_votos(
    banco_de_dados: Banco_de_Dados, servidor: socket.socket, evento_parar: threading.Event
) -> None:
    """Laço de repetição para receber os votos dos participantes."""
    print("Limpando buffer de mensagens antigas...")
    while True:
        try:
            # Descarta dados antigos no buffer para evitar leitura de votos de pautas passadas
            servidor.recvfrom(1024)
        except socket.timeout:
            print("Buffer limpo. Pronto para receber votos.")
            break
            
    print("Aguardando votos...")
    while not evento_parar.is_set():
        try:
            dado, votante = servidor.recvfrom(1000)
            try:
                print("Voto recebido, tentando decodificar...")
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
    servidor: socket.socket,
    pauta: str,
    enviar: bool = True,
) -> str:
    """Compila e formata a string com o resultado da votação de uma pauta."""
    resultado = "-----------------Resultado da votação!-----------------\n"
    resultado += f"Pauta discutida: |{pauta}|\n"
    qtd_a_favor = banco_de_dados.dados["pautas"][pauta]["qtd de votos a favor"]
    qtd_contra = banco_de_dados.dados["pautas"][pauta]["qtd de votos contra"]
    qtd_abstenção = banco_de_dados.dados["pautas"][pauta]["qtd de votos anulados"]
    total = qtd_a_favor + qtd_contra + qtd_abstenção

    if total == 0:
        porcentagem_a_favor = 0.0
        porcentagem_contra = 0.0
        porcentagem_abstenção = 0.0
    else:
        porcentagem_a_favor = (qtd_a_favor / total) * 100
        porcentagem_contra = (qtd_contra / total) * 100
        porcentagem_abstenção = (qtd_abstenção / total) * 100

    resultado += f"Votos a favor = {porcentagem_a_favor:.2f}%\n"
    resultado += f"Votos contra = {porcentagem_contra:.2f}%\n"
    resultado += f"Abstenções = {porcentagem_abstenção:.2f}%\n"
    resultado += "-------------------------------------------------------------------\n\n"

    if enviar:
        mandar_mensagem(banco_de_dados, servidor, resultado)

    return resultado


def aguardar_votantes(
    servidor: socket.socket,
) -> tuple[Banco_de_Dados, threading.Thread, threading.Event]:
    """Inicia a thread para aguardar a entrada de votantes."""
    evento_encerrar_espera = threading.Event()
    banco_de_dados = Banco_de_Dados()
    processo = threading.Thread(
        target=receber_votantes,
        args=(banco_de_dados, servidor, evento_encerrar_espera),
    )
    processo.start()
    return (banco_de_dados, processo, evento_encerrar_espera)


def aguardar_votos(
    banco_de_dados: Banco_de_Dados, servidor: socket.socket
) -> tuple[threading.Thread, threading.Event]:
    """Inicia a thread para aguardar os votos dos participantes."""
    evento_encerrar_votacao = threading.Event()
    processo = threading.Thread(
        target=receber_votos, args=(banco_de_dados, servidor, evento_encerrar_votacao)
    )
    processo.start()
    return (processo, evento_encerrar_votacao)