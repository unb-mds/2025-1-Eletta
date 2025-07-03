import socket
import json

server_addr = ("127.0.0.1", 5555)


def verificar_host_ativo() -> bool:
    """
    Usa broadcast UDP para descobrir se há um host ativo na rede.
    Se houver, atualiza `server_addr` com o IP do host.
    """
    global server_addr
    try:
        # Cria um socket UDP com broadcast habilitado
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        test_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        test_socket.settimeout(2.0)

        # Endereço de broadcast (pode adaptar à sua rede se necessário)
        broadcast_addr = ("255.255.255.255", 5555)
        mensagem = "host_check"
        test_socket.sendto(mensagem.encode(), broadcast_addr)

        # Tenta receber resposta do host
        response, addr = test_socket.recvfrom(1024)
        if response.decode().strip() == "host_active":
            print(f"Host descoberto no IP: {addr[0]}")
            server_addr = (addr[0], 5555)  # Atualiza com IP real do host
            return True

        return False
    except socket.timeout:
        return False
    except Exception as e:
        print(f"Erro ao tentar descobrir host: {e}")
        return False
    finally:
        test_socket.close()


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
