import socket

def send_vote():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 5000)
    
    print("Opções: a favor, contra, abster")
    while True:
        vote = input("Digite seu voto: ").strip().lower()
        if vote in ['sair', 'exit']:
            break
            
        sock.sendto(vote.encode(), server_address)
        print(f"Voto '{vote}' enviado!")

if __name__ == "__main__":
    send_vote()