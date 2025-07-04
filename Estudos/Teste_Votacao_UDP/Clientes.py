import socket
import uuid

# Configuração do cliente
SERVER = "127.0.0.1"  # IP do servidor (sem http://)
PORT = 5000

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    user_id = str(uuid.uuid4())  # Gera um ID único para o cliente
    print(f"Seu ID único: {user_id}")

    while True:
        print("\nOpções de voto: a_favor, contra, abstencao")
        vote = input("Digite seu voto (ou 'sair' para encerrar): ").strip()

        if vote.lower() == "sair":
            print("Encerrando o cliente de votação.")
            break

        message = f"{user_id}:{vote}"
        client.sendto(message.encode("utf-8"), (SERVER, PORT))

        response, _ = client.recvfrom(1024)
        print("Resposta do servidor:", response.decode("utf-8"))

if __name__ == "__main__":
    main()