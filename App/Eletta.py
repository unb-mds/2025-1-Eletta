import flet as ft

from controlador import controller
from views import host, home, votante


def principal(pagina: ft.Page) -> None:
    controlador = controller.Controlador(pagina)

    def mudar_de_pagina(e: ft.ControlEvent) -> None:
        if pagina.route not in [
            "/votacao",
            "/confirmacao",
            "/sucesso_voto_computado",
            "/tempo_esgotado",
        ]:
            if hasattr(controlador, "parar_contagem_regressiva_votante"):
                controlador.parar_contagem_regressiva_votante()

        pagina.views.clear()
        if pagina.route == "/":
            pagina.views.append(home.pagina_inicial(pagina, controlador))
        elif pagina.route == "/espera":
            pagina.views.append(votante.pagina_de_espera(pagina))
        elif pagina.route == "/aguardar_host":
            pagina.views.append(votante.aguardar_host(pagina))
        elif pagina.route == "/atencao_votante":
            pagina.views.append(votante.pagina_de_atencao(pagina, controlador))
        elif pagina.route == "/votacao":
            pagina.views.append(votante.pagina_de_votacao(pagina, controlador))
            if hasattr(controlador, "iniciar_contagem_regressiva_votante"):
                controlador.iniciar_contagem_regressiva_votante()
        elif pagina.route == "/tempo_esgotado":
            pagina.views.append(votante.pagina_tempo_esgotado(pagina))
        elif pagina.route == "/confirmacao":
            pagina.views.append(
                votante.pagina_de_confirmacao(
                    pagina, controlador, controlador.voto_pendente
                )
            )
        elif pagina.route == "/espera_votantes":
            pagina.views.append(host.pagina_de_espera_votantes(pagina, controlador))
        elif pagina.route == "/criacao_de_pauta":
            pagina.views.append(host.pagina_de_criacao_de_pauta(pagina, controlador))
        elif pagina.route == "/espera_votos":
            pagina.views.append(host.pagina_de_espera_votos(pagina, controlador))
        elif pagina.route == "/resultado":
            pagina.views.append(home.pagina_do_resultado(pagina, controlador.mensagem))
        elif pagina.route == "/resultado_host_intermediario":
            pagina.views.append(
                host.pagina_do_resultado_host_intermediario(pagina, controlador)
            )
        elif pagina.route == "/resultado_host_final":
            pagina.views.append(
                host.pagina_do_resultado_host_final(pagina, controlador)
            )
        elif pagina.route == "/sucesso_criacao_sala":
            pagina.views.append(host.pagina_sucesso_criacao_sala(pagina))
        elif pagina.route == "/sucesso_voto_computado":
            pagina.views.append(votante.pagina_sucesso_voto_computado(pagina))

        pagina.update()

    pagina.on_route_change = mudar_de_pagina
    pagina.go("/")


if __name__ == "__main__":
    ft.app(target=principal, assets_dir="assets")
