import flet as ft
from controlador import controller
from views import votante, host, home


def main(page: ft.Page) -> None:
    controlador = controller.Controlador(page)

    def mudar_de_pagina(e: ft.ControlEvent) -> None:
        page.views.clear()
        if page.route == "/":
            page.views.append(home.pagina_inicial(page, controlador))

        elif page.route == "/espera":
            page.views.append(votante.pagina_de_espera(page))

        elif page.route == "/votacao":
            page.views.append(votante.pagina_de_votacao(page, controlador))

        elif page.route == "/confirmacao":
            page.views.append(
                votante.pagina_de_confirmacao(
                    page, controlador, controlador.voto_pendente
                )
            )

        elif page.route == "/espera_votantes":
            page.views.append(host.pagina_de_espera_votantes(page, controlador))

        elif page.route == "/criacao_de_pauta":
            page.views.append(host.pagina_de_criacao_de_pauta(e.page, controlador))

        elif page.route == "/espera_votos":
            page.views.append(host.pagina_de_espera_votos(page, controlador))

        elif page.route == "/resultado":
            page.views.append(home.pagina_do_resultado(page, controlador.mensagem))

        page.update()

    page.on_route_change = mudar_de_pagina
    page.go("/")

ft.app(target=main, assets_dir="assets") #Lê o diretório

