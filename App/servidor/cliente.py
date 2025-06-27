import socket
import json

server_addr = ("127.0.0.1", 5555)


def verificar_host_ativo() -> bool:
    """
    Verifica se existe um host ativo na rede tentando conectar na porta 5555.
    Retorna True se houver um host ativo, False caso contrário.
    """
    try:
        # Cria um socket temporário para testar a conexão
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        test_socket.settimeout(1.0)  # Timeout de 1s para esperar resposta

        # Tenta enviar uma mensagem de teste
        test_message = "host_check"
        test_socket.sendto(test_message.encode(), server_addr)

        # Tenta receber uma resposta do servidor
        try:
            response, addr = test_socket.recvfrom(1024)
            test_socket.close()
            return True  # Se recebeu resposta, há um host ativo
        except socket.timeout:
            # Se não recebeu resposta, não há host ativo
            test_socket.close()
            return False

    except (ConnectionRefusedError, OSError):
        # Se der qualquer erro, significa que não há host ativo
        return False
    except Exception:
        # Para qualquer outro erro, assume que não há host
        return False


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
