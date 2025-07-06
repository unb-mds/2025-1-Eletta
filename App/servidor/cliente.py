import socket
import json

# Endereço padrão do servidor, atualizado quando o host é descoberto
endereco_servidor = ("127.0.0.1", 5555)


def obter_ip_broadcast() -> str:
    """
    Descobre o endereço de IP local e o converte para um endereço de broadcast.
    Ex: 192.168.1.5 -> 192.168.1.255
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Conecta-se a um IP externo para descobrir o IP local da interface de rede principal
        s.connect(("8.8.8.8", 80))
        ip_local = s.getsockname()[0]
    except Exception:
        ip_local = "127.0.0.1"  # Retorna o localhost em caso de falha
    finally:
        s.close()

    partes_ip = ip_local.split(".")
    partes_ip[-1] = "255"  # Substitui o último octeto por 255
    return ".".join(partes_ip)


def verificar_host_ativo() -> bool:
    """
    Envia uma mensagem de broadcast para descobrir se há um host ativo na rede.
    """
    global endereco_servidor
    socket_teste = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        socket_teste.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        socket_teste.settimeout(2.0)

        ip_broadcast = obter_ip_broadcast()
        endereco_broadcast = (ip_broadcast, 5555)

        # Mensagem de verificação (protocolo)
        mensagem = "host_check"
        socket_teste.sendto(mensagem.encode(), endereco_broadcast)

        resposta, endereco = socket_teste.recvfrom(1024)
        if resposta.decode().strip() == "host_active":
            print(f"Host descoberto no IP: {endereco[0]}")
            endereco_servidor = (endereco[0], 5555)  # Atualiza o endereço do servidor
            return True

        return False
    except socket.timeout:
        # Se não houver resposta em 2 segundos, assume-se que não há host
        return False
    except Exception as e:
        print(f"Erro ao tentar descobrir host: {e}")
        return False
    finally:
        socket_teste.close()


def virar_votante() -> socket.socket:
    """
    Cria um socket para o votante e notifica o servidor da sua entrada.
    """
    votante = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Mensagem de entrada (protocolo)
    mensagem_entrada = "joined"
    votante.sendto(mensagem_entrada.encode(), endereco_servidor)
    return votante


def receber_mensagem(votante: socket.socket) -> str:
    """
    Aguarda e recebe uma mensagem do servidor.
    """
    dados, remetente = votante.recvfrom(1024)
    mensagem = dados.decode()
    return mensagem


def votar(votante: socket.socket, voto: str, pauta: str) -> None:
    """
    Envia o voto para o servidor no formato JSON.
    """
    dados_voto = [voto, pauta]
    voto_em_json = json.dumps(dados_voto)
    votante.sendto(voto_em_json.encode(), endereco_servidor)