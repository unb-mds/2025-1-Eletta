import socket
import threading
import flet as ft

PORTA = 5000
IP_SERVIDOR = "192.168.1.80"  # <<< Coloque aqui o IP da máquina do servidor

def main(page: ft.Page):
    page.title = "Cliente de Votação UDP"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    pergunta_text = ft.Text("Clique em 'Conectar' para começar", size=16, color="blue")
    status = ft.Text("", size=16)
    ja_votou = False
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)

    def receber_mensagens():
        nonlocal ja_votou
        while True:
            try:
                data, _ = sock.recvfrom(1024)
                if data.startswith(b"PERGUNTA|"):
                    pergunta = data.decode().split("|", 1)[1]
                    pergunta_text.value = pergunta
                    ja_votou = False
                    status.value = "Nova pergunta recebida! Você pode votar agora."
                    status.color = "green"
                    page.update()
            except socket.timeout:
                continue
            except Exception as e:
                status.value = f"Erro na conexão: {e}"
                status.color = "red"
                page.update()
                break

    def conectar_servidor(e=None):
        nonlocal ja_votou
        try:
            endereco = (IP_SERVIDOR, PORTA)
            sock.sendto("CONECT|".encode(), endereco)
            ja_votou = False
            status.value = "Conectado! Aguardando perguntas..."
            status.color = "blue"
            page.update()
            threading.Thread(target=receber_mensagens, daemon=True).start()
        except Exception as e:
            status.value = f"Falha na conexão: {e}"
            status.color = "red"
            page.update()

    def enviar_voto(voto):
        nonlocal ja_votou
        if ja_votou:
            status.value = "❌ Você já votou nesta pergunta!"
            status.color = "red"
            page.update()
            return

        if "Aguardando" in pergunta_text.value:
            status.value = "❌ Nenhuma pergunta disponível para votar!"
            status.color = "red"
            page.update()
            return

        try:
            sock.sendto(f"{pergunta_text.value}|{voto}".encode(), (IP_SERVIDOR, PORTA))
            status.value = f"✅ Voto '{voto}' enviado!"
            status.color = "green"
            ja_votou = True
        except Exception as e:
            status.value = f"❌ Falha ao enviar: {e}"
            status.color = "red"
        page.update()

    page.add(
        ft.Column([
            ft.ElevatedButton("🔌 Conectar", on_click=conectar_servidor),
            ft.Divider(),
            pergunta_text,
            ft.Divider(),
            ft.Row([
                ft.ElevatedButton("✅ A Favor", on_click=lambda _: enviar_voto("a favor")),
                ft.ElevatedButton("❌ Contra", on_click=lambda _: enviar_voto("contra")),
                ft.ElevatedButton("🤔 Abster", on_click=lambda _: enviar_voto("abster")),
            ], alignment="center"),
            status
        ], alignment="center")
    )

ft.app(target=main, view=ft.WEB_BROWSER, port=8550)

