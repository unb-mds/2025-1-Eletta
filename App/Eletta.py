import flet as ft
from controlador import controller
from views import votante, host, home


def main(page: ft.Page) -> None:
    controlador = controller.Controlador(page)

    def mudar_de_pagina(e: ft.ControlEvent) -> None:
        current_route = page.route

        if (
            hasattr(controlador, "stop_voter_countdown")
            and hasattr(controlador, "timer_thread_votante")
            and controlador.timer_thread_votante is not None
            and current_route != "/votacao"
        ):
            controlador.stop_voter_countdown()

        page.views.clear()

        if current_route == "/":
            page.views.append(home.pagina_inicial(page, controlador))

        elif current_route == "/espera":
            page.views.append(votante.pagina_de_espera(page))

        elif current_route == "/votacao":
            view = votante.pagina_de_votacao(page, controlador)
            page.views.append(view)
            if hasattr(controlador, "start_voter_countdown"):
                controlador.start_voter_countdown()

        elif current_route == "/confirmacao":
            voto_a_confirmar = (
                controlador.voto_pendente
                if hasattr(controlador, "voto_pendente")
                else "Indefinido"
            )
            page.views.append(
                votante.pagina_de_confirmacao(page, controlador, voto_a_confirmar)
            )

        elif current_route == "/espera_votantes":
            page.views.append(host.pagina_de_espera_votantes(page, controlador))

        elif current_route == "/criacao_de_pauta":
            page.views.append(host.pagina_de_criacao_de_pauta(page, controlador))

        elif current_route == "/espera_votos":
            page.views.append(host.pagina_de_espera_votos(page, controlador))

        elif current_route == "/resultado":
            resultado_msg = (
                controlador.mensagem
                if hasattr(controlador, "mensagem") and controlador.mensagem
                else "Resultado não disponível."
            )
            page.views.append(home.pagina_do_resultado(page, resultado_msg))

        page.update()

    page.on_route_change = mudar_de_pagina
    page.go("/")


ft.app(target=main, assets_dir="assets")