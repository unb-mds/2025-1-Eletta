import socket
import json
from datetime import datetime
import os
from collections import defaultdict
from cryptography.fernet import Fernet  # Para criptografia

# ===== CONFIGURAÇÕES =====
ARQUIVO_VOTOS = "votos.json"
CHAVE_CRIPTOGRAFIA = "chave_cripto.key"  # Arquivo com a chave AES ...

# ===== CRIPTOGRAFIA =====
class Criptografia:
    @staticmethod
    def gerar_chave():
        """Gera/salva uma chave AES se não existir"""
        if not os.path.exists(CHAVE_CRIPTOGRAFIA):
            chave = Fernet.generate_key()
            with open(CHAVE_CRIPTOGRAFIA, "wb") as f:
                f.write(chave)
        return open(CHAVE_CRIPTOGRAFIA, "rb").read()

    def __init__(self):
        self.cipher = Fernet(self.gerar_chave())

    def criptografar(self, texto):
        return self.cipher.encrypt(texto.encode()).decode()

    def descriptografar(self, texto_cripto):
        return self.cipher.decrypt(texto_cripto.encode()).decode()

# ===== SERVIDOR DE VOTAÇÃO =====
class ServidorVotacao:
    def __init__(self, host="0.0.0.0", port=5000):
        self.host = host
        self.port = port
        self.crypto = Criptografia()  # Instância de criptografia
        self.votos = self._carregar_votos()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _carregar_votos(self):
        """Carrega votos do JSON ou cria um novo arquivo"""
        if os.path.exists(ARQUIVO_VOTOS):
            try:
                with open(ARQUIVO_VOTOS, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"⚠️ Erro ao carregar votos: {e}. Criando novo arquivo.")
        
        return {"total": defaultdict(int), "historico": []}

    def _salvar_votos(self):
        """Salva votos no JSON com tratamento de erros"""
        try:
            with open(ARQUIVO_VOTOS, "w") as f:
                json.dump(
                    {
                        "total": dict(self.votos["total"]),
                        "historico": self.votos["historico"],
                    },
                    f,
                    indent=2,
                    ensure_ascii=False,
                )
        except IOError as e:
            print(f"❌ Falha ao salvar votos: {e}")

    def _processar_voto(self, voto, endereco_ip, porta):
        """Valida, criptografa e registra o voto"""
        voto = voto.strip().lower()
        mapeamento = {
            "sim": "a_favor",
            "s": "a_favor",
            "a favor": "a_favor",
            "não": "contra",
            "nao": "contra",
            "n": "contra",
            "contra": "contra",
            "abster": "abstencao",
            "abs": "abstencao",
        }

        if voto not in mapeamento:
            return False

        # Criptografa o IP
        ip_cripto = self.crypto.criptografar(endereco_ip)

        # Registra o voto
        self.votos["total"][mapeamento[voto]] += 1
        self.votos["historico"].append(
            {
                "tipo": mapeamento[voto],
                "endereco_cripto": ip_cripto,  # IP criptografado
                "porta": porta,  # Porta em claro (opcional)
                "timestamp": datetime.now().isoformat(),
                "voto_original": voto,
            }
        )
        self._salvar_votos()
        return True

    def iniciar(self):
        """Inicia o servidor UDP"""
        self.socket.bind((self.host, self.port))
        print(f"✅ Servidor ativo em {self.host}:{self.port}")
        print("📊 Aguardando votos (Ctrl+C para sair)...")

        try:
            while True:
                data, addr = self.socket.recvfrom(1024)
                ip, porta = addr
                voto = data.decode()

                if self._processar_voto(voto, ip, porta):
                    print(f"🗳️ Voto de {ip}: {voto.upper()}")
                    print(f"📊 Totais: {dict(self.votos['total'])}")
                else:
                    print(f"⚠️ Voto inválido de {ip}: '{voto}'")

        except KeyboardInterrupt:
            print("\n🛑 Servidor encerrado.")
        finally:
            self.socket.close()
 
 
 #PARA DESCRIPTOGRAFAR            
#from cryptography.fernet import Fernet

#chave = open("chave_cripto.key", "rb").read()
#cipher = Fernet(chave)

#with open("votos.json") as f:
 #   dados = json.load(f)

#for voto in dados["historico"]:
#    ip_real = cipher.decrypt(voto["endereco_cripto"].encode()).decode()
#    print(f"{ip_real}:{voto['porta']} -> {voto['tipo']}")      
            
            
            

# ===== EXECUÇÃO =====
if __name__ == "__main__":
    servidor = ServidorVotacao()
    servidor.iniciar()