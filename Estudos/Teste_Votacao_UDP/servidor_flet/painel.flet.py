import json
import flet as ft
import time

ARQUIVO_VOTOS = "votos.json"

def main(page: ft.Page):
    page.title = "Painel de Votação"
    page.window_width = 600
    page.window_height = 500

    votos_texto = ft.Text("Carregando votos...", size=20)
    historico = ft.ListView(expand=True, spacing=10, padding=10)

    def carregar_votos():
        try:
            with open(ARQUIVO_VOTOS, "r") as f:
                dados = json.load(f)
            votos = dados.get("total", {})
            votos_texto.value = f"A Favor: {votos.get('a_favor',0)} | Contra: {votos.get('contra',0)} | Abster: {votos.get('abstencao',0)}"

            historico.controls = [
                ft.Text(f"[{v['timestamp']}] {v.get('pergunta', 'Pergunta não definida')} - {v['tipo'].upper()}", size=12)
                for v in dados.get("historico", [])[-10:]
            ]
        except Exception:
            votos_texto.value = "Nenhum voto recebido ainda."

        page.update()

    def atualizar_loop():
        while True:
            carregar_votos()
            time.sleep(2)

    page.add(
        ft.Column([
            votos_texto,
            ft.Divider(),
            ft.Text("Últimos votos:", size=16),
            historico
        ])
    )

    import threading
    threading.Thread(target=atualizar_loop, daemon=True).start()

ft.app(target=main)
