import socket
import threading
import json
import os
from datetime import datetime
from collections import defaultdict
from cryptography.fernet import Fernet
import flet as ft

# ===== CONFIGURAÇÕES =====
ARQUIVO_VOTOS = "votos.json"
CHAVE_CRIPTOGRAFIA = "chave_cripto.key"
PORTA = 5000

# ===== CLASSE DE CRIPTOGRAFIA =====
class Criptografia:
    def __init__(self):
        if not os.path.exists(CHAVE_CRIPTOGRAFIA):
            chave = Fernet.generate_key()
            with open(CHAVE_CRIPTOGRAFIA, "wb") as f:
                f.write(chave)
        self.cipher = Fernet(open(CHAVE_CRIPTOGRAFIA, "rb").read())

    def criptografar(self, texto):
        return self.cipher.encrypt(texto.encode()).decode()

# ===== SERVIDOR DE VOTAÇÃO =====
class ServidorVotacao:
    def __init__(self, atualizar_ui_callback):
        self.host = "0.0.0.0"
        self.port = PORTA
        self.crypto = Criptografia()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ativo = False
        self.votos = self._carregar_votos()
        self.atualizar_ui = atualizar_ui_callback
        self.pergunta_atual = "Nenhuma pergunta definida"
        self.clientes_conectados = set()
        self.clientes_que_votaram = set()

    def definir_pergunta(self, pergunta):
        self.pergunta_atual = pergunta
        self.clientes_que_votaram.clear()
        threading.Thread(target=self._enviar_pergunta_a_todos, daemon=True).start()  # Envia em uma thread separada
        self.atualizar_ui()
        return True

    def _enviar_pergunta_a_todos(self):
        for addr in list(self.clientes_conectados):  # Usa uma cópia da lista para evitar problemas de concorrência
            try:
                self.socket.sendto(f"PERGUNTA|{self.pergunta_atual}".encode(), addr)
            except:
                self.clientes_conectados.discard(addr)  # Remove clientes inativos
        
    def _carregar_votos(self):
        if os.path.exists(ARQUIVO_VOTOS):
            try:
                with open(ARQUIVO_VOTOS, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"total": defaultdict(int), "historico": []}

    def _salvar_votos(self):
        with open(ARQUIVO_VOTOS, "w") as f:
            json.dump(
                {
                    "total": dict(self.votos["total"]),
                    "historico": self.votos["historico"]
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

    def _processar_voto(self, mensagem, ip, porta):
        try:
            pergunta, voto = mensagem.split("|", 1)
            voto = voto.strip().lower()
            opcoes = {
                "a favor": "a_favor",
                "contra": "contra",
                "abster": "abstencao",
            }
            if voto not in opcoes:
                return False

            cliente_id = f"{ip}:{porta}"
            if cliente_id in self.clientes_que_votaram:
                return False

            ip_cripto = self.crypto.criptografar(ip)
            self.votos["total"][opcoes[voto]] += 1
            self.votos["historico"].append({
                "pergunta": pergunta,
                "tipo": opcoes[voto],
                "endereco_cripto": ip_cripto,
                "porta": porta,
                "timestamp": datetime.now().isoformat()
            })
            self.clientes_que_votaram.add(cliente_id)
            self._salvar_votos()
            self.atualizar_ui()
            return True
        except Exception as e:
            print(f"Erro ao processar voto: {e}")
            return False

    def iniciar(self):
        def loop_servidor():
            try:
                self.socket.bind((self.host, self.port))
                self.ativo = True
                self.atualizar_ui()
                while self.ativo:
                    data, addr = self.socket.recvfrom(1024)
                    mensagem = data.decode()
                    
                    if mensagem.startswith("CONECT|"):
                        self.clientes_conectados.add(addr)
                        self.socket.sendto(f"PERGUNTA|{self.pergunta_atual}".encode(), addr)
                    else:
                        self._processar_voto(mensagem, addr[0], addr[1])
            except Exception as e:
                print(f"Erro no servidor: {e}")
            finally:
                self.socket.close()

        threading.Thread(target=loop_servidor, daemon=True).start()

    def parar(self):
        self.ativo = False
        self.socket.close()

# ===== INTERFACE COM FLET =====
def main(page: ft.Page):
    page.title = "Servidor de Votação UDP"
    page.window_width = 800
    page.window_height = 600

    status_text = ft.Text("Servidor parado", size=18, color="red")
    votos_totais = ft.Text("Totais: {}", size=16)
    historico_list = ft.ListView(expand=True, spacing=10, padding=20)

    pergunta_input = ft.TextField(label="Nova pergunta", width=400)

    def definir_pergunta(e):
        if servidor.definir_pergunta(pergunta_input.value):
            pergunta_input.value = ""
            page.update()

    def iniciar(e):
        servidor.iniciar()
        status_text.value = "Servidor rodando"
        status_text.color = "green"
        page.update()

    def parar(e):
        servidor.parar()
        status_text.value = "Servidor parado"
        status_text.color = "red"
        page.update()

    page.add(
        ft.Column(
            [
                status_text,
                ft.Row([
                    ft.ElevatedButton("Iniciar Servidor", on_click=iniciar),
                    ft.ElevatedButton("Parar Servidor", on_click=parar),
                ], alignment="center"),
                pergunta_input,
                ft.ElevatedButton("Definir Pergunta", on_click=definir_pergunta),
                votos_totais,
                historico_list,
            ],
            expand=True,
        )
    )

    def atualizar_ui():
        votos = servidor.votos["total"]
        votos_totais.value = f"Totais: {dict(votos)}"
        historico_list.controls = [
            ft.Text(f"[{v['timestamp']}] {v['tipo'].upper()} - {v.get('pergunta', '')}", size=12)
            for v in servidor.votos["historico"]
        ]
        page.update()

    servidor = ServidorVotacao(atualizar_ui)

ft.app(target=main)