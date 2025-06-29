import flet as ft

from controlador import controller
from views import host, home, votante


def main(page: ft.Page) -> None:
    controlador = controller.Controlador(page)

    def mudar_de_pagina(e: ft.ControlEvent) -> None:
        """
        Gerencia a navegação entre as diferentes telas (Views) da aplicação,
        limpando as visualizações anteriores e adicionando a nova de acordo
        com a rota atual.
        """

        # Garante que a thread de contagem regressiva do votante seja
        # interrompida ao navegar para telas onde ela não é necessária.
        # Isso evita que a aplicação congele ou se comporte de forma inesperada.
        if page.route not in [
            "/votacao",
            "/confirmacao",
            "/sucesso_voto_computado",
            "/tempo_esgotado",
        ]:
            if hasattr(controlador, "parar_contagem_regressiva_votante"):
                controlador.parar_contagem_regressiva_votante()

        page.views.clear()
        if page.route == "/":
            page.views.append(home.pagina_inicial(page, controlador))

        elif page.route == "/espera":
            page.views.append(votante.pagina_de_espera(page))

        elif page.route == "/aguardar_host":
            page.views.append(votante.aguardar_host(page))

        elif page.route == "/atencao_votante":
            page.views.append(votante.pagina_de_atencao(page, controlador))

        elif page.route == "/votacao":
            page.views.append(votante.pagina_de_votacao(page, controlador))
            if hasattr(controlador, "iniciar_contagem_regressiva_votante"):
                controlador.iniciar_contagem_regressiva_votante()

        # --- Rota Adicionada ---
        elif page.route == "/tempo_esgotado":
            page.views.append(votante.pagina_tempo_esgotado(page))
        # --- Fim da Rota ---

        elif page.route == "/confirmacao":
            page.views.append(
                votante.pagina_de_confirmacao(
                    page, controlador, controlador.voto_pendente
                )
            )

        elif page.route == "/espera_votantes":
            page.views.append(host.pagina_de_espera_votantes(page, controlador))

        elif page.route == "/criacao_de_pauta":
            page.views.append(host.pagina_de_criacao_de_pauta(page, controlador))

        elif page.route == "/espera_votos":
            page.views.append(host.pagina_de_espera_votos(page, controlador))

        elif page.route == "/resultado":
            page.views.append(home.pagina_do_resultado(page, controlador.mensagem))

        elif page.route == "/resultado_host_intermediario":
            page.views.append(
                host.pagina_do_resultado_host_intermediario(page, controlador)
            )

        elif page.route == "/resultado_host_final":
            page.views.append(host.pagina_do_resultado_host_final(page, controlador))

        elif page.route == "/sucesso_criacao_sala":
            page.views.append(host.pagina_sucesso_criacao_sala(page))

        elif page.route == "/sucesso_voto_computado":
            page.views.append(votante.pagina_sucesso_voto_computado(page))

        page.update()

    page.on_route_change = mudar_de_pagina
    page.go("/")


if __name__ == "__main__":
    # Inicia a aplicação Flet, especificando o diretório de assets (imagens, etc.)
    ft.app(target=main, assets_dir="assets")
