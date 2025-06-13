import socket
import threading
import flet as ft

PORTA = 5000

def main(page: ft.Page):
    page.title = "Cliente de Votação UDP"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    # Elementos da UI
    ip_input = ft.TextField(label="IP do servidor", value="127.0.0.1", width=300)
    pergunta_text = ft.Text("Aguardando conexão...", size=16, color="blue")
    status = ft.Text("", size=16)
    ja_votou = False  # Flag para controlar se o cliente já votou na pergunta atual
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)

    # Thread para receber mensagens do servidor
    def receber_mensagens():
        nonlocal ja_votou
        while True:
            try:
                data, _ = sock.recvfrom(1024)
                if data.startswith(b"PERGUNTA|"):
                    pergunta = data.decode().split("|", 1)[1]
                    pergunta_text.value = pergunta
                    ja_votou = False  # Reinicia a flag quando uma nova pergunta é recebida
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

    # Conectar ao servidor
    def conectar_servidor():
        nonlocal ja_votou
        try:
            endereco = (ip_input.value.strip(), PORTA)
            sock.sendto("CONECT|".encode(), endereco)
            ja_votou = False  # Reinicia a flag ao conectar
            status.value = "Conectado! Aguardando perguntas..."
            status.color = "blue"
            page.update()
            
            # Inicia a thread de recebimento
            threading.Thread(target=receber_mensagens, daemon=True).start()
        except Exception as e:
            status.value = f"Falha na conexão: {e}"
            status.color = "red"
            page.update()

    # Enviar voto
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
            sock.sendto(f"{pergunta_text.value}|{voto}".encode(), (ip_input.value.strip(), PORTA))
            status.value = f"✅ Voto '{voto}' enviado!"
            status.color = "green"
            ja_votou = True
        except Exception as e:
            status.value = f"❌ Falha ao enviar: {e}"
            status.color = "red"
        page.update()

    # Layout
    page.add(
        ft.Column([
            ip_input,
            ft.ElevatedButton("Conectar", on_click=lambda _: conectar_servidor()),
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

ft.app(target=main)