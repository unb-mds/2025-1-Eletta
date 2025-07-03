from servidor.cliente import verificar_host_ativo, virar_votante, receber_mensagem
from servidor.servidor import ip_local
import time

if __name__ == "__main__":
    local_ip = ip_local()
    print(f"Seu IP local é: {local_ip}")

    print("🔍 Procurando host na rede...")

    if verificar_host_ativo():
        print("✅ Host encontrado!")

        socket_votante = virar_votante()
        print("🔄 Votante conectado. Aguardando mensagem do host...")

        try:
            # Aguarda por mensagem do host por até 10 segundos
            socket_votante.settimeout(10.0)
            mensagem = receber_mensagem(socket_votante)
            print(f"📩 Mensagem recebida: {mensagem}")
        except Exception as e:
            print(f"❌ Erro ao receber mensagem: {e}")
    else:
        print("❌ Nenhum host foi encontrado.")