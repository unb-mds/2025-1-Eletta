import socket
import json

server_addr = ("127.0.0.1", 5555)


def get_broadcast_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1"
    finally:
        s.close()

    ip_parts = local_ip.split(".")
    ip_parts[-1] = "255"
    return ".".join(ip_parts)


def verificar_host_ativo() -> bool:
    global server_addr
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        test_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        test_socket.settimeout(2.0)

        broadcast_ip = get_broadcast_ip()
        broadcast_addr = (broadcast_ip, 5555)

        mensagem = "host_check"
        test_socket.sendto(mensagem.encode(), broadcast_addr)

        response, addr = test_socket.recvfrom(1024)
        if response.decode().strip() == "host_active":
            print(f"Host descoberto no IP: {addr[0]}")
            server_addr = (addr[0], 5555)
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
