import flet as ft
from controlador import controller
from views import votante, host, home


def main(page: ft.Page) -> None:
    """
    Função principal que inicializa a aplicação Flet.

    Args:
        page (ft.Page): A página principal da aplicação.
    """
    controlador = controller.Controlador(page)

    def mudar_de_pagina(e: ft.ControlEvent) -> None:
        """
        Gerencia a navegação entre as diferentes visualizações (páginas) da aplicação.

        Args:
            e (ft.ControlEvent): O evento que acionou a mudança de rota.
        """
        # --- Correção ---
        # Isso garante que a thread que escuta o resultado da votação não seja
        # encerrada prematuramente quando o usuário vota com sucesso ou quando
        # o tempo se esgota, o que era a causa do congelamento da tela.
        if page.route not in [
            "/votacao",
            "/confirmacao",
            "/sucesso_voto_computado",
            "/tempo_esgotado",
        ]:
            if hasattr(controlador, "parar_contagem_regressiva_votante"):
                controlador.parar_contagem_regressiva_votante()
        # --- Fim da Correção ---

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

        elif page.route == "/resultado_host":
            page.views.append(host.pagina_do_resultado_host(page, controlador))

        elif page.route == "/sucesso_criacao_sala":
            page.views.append(host.pagina_sucesso_criacao_sala(page))

        elif page.route == "/sucesso_voto_computado":
            page.views.append(votante.pagina_sucesso_voto_computado(page))

        page.update()

    page.on_route_change = mudar_de_pagina
    page.go("/")


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")  # Lê o diretório
