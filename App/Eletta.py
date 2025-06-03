import flet as ft
from controlador import controller # Assumindo que controller.py está no diretório 'controlador'
from views import votante, host, home

def main(page: ft.Page) -> None:
    controlador = controller.Controlador(page) # Instanciação corrigida se necessário

    def mudar_de_pagina(e: ft.ControlEvent) -> None:
        current_route = page.route # A nova rota para a qual estamos navegando

        # Para o cronômetro do votante se estiver navegando para fora da página de votação
        # Verifica a existência do atributo por segurança durante a inicialização ou se o controlador mudar
        if hasattr(controlador, 'stop_voter_countdown') and \
           hasattr(controlador, 'timer_thread_votante') and \
           controlador.timer_thread_votante is not None and \
           current_route != "/votacao": # Para somente se a nova rota NÃO for /votacao
            controlador.stop_voter_countdown()

        page.views.clear()

        if current_route == "/":
            page.views.append(home.pagina_inicial(page, controlador))

        elif current_route == "/espera":
            page.views.append(votante.pagina_de_espera(page))

        elif current_route == "/votacao":
            # A função pagina_de_votacao atribuirá seu controle de cronômetro Text
            # para controlador.timer_control_votante
            view = votante.pagina_de_votacao(page, controlador)
            page.views.append(view)
            # Agora que a view foi construída e timer_control_votante está (espera-se) definido, inicia a contagem regressiva.
            if hasattr(controlador, 'start_voter_countdown'):
                controlador.start_voter_countdown()

        elif current_route == "/confirmacao":
            # Garante que voto_pendente esteja disponível; pode precisar de tratamento robusto se a navegação ocorrer diretamente
            voto_a_confirmar = controlador.voto_pendente if hasattr(controlador, 'voto_pendente') else "Indefinido"
            page.views.append(votante.pagina_de_confirmacao(page, controlador, voto_a_confirmar))

        elif current_route == "/espera_votantes":
            page.views.append(host.pagina_de_espera_votantes(page, controlador))

        elif current_route == "/criacao_de_pauta":
            # Passa e.page se é isso que pagina_de_criacao_de_pauta espera, ou apenas page
            page.views.append(host.pagina_de_criacao_de_pauta(page, controlador))


        elif current_route == "/espera_votos":
            page.views.append(host.pagina_de_espera_votos(page, controlador))

        elif current_route == "/resultado":
            # Usando home.pagina_do_resultado conforme a estrutura existente de Eletta.py
            # Garante que controlador.mensagem tenha a string de resultado
            resultado_msg = controlador.mensagem if hasattr(controlador, 'mensagem') and controlador.mensagem else "Resultado não disponível."
            page.views.append(home.pagina_do_resultado(page, resultado_msg))

        page.update()

    page.on_route_change = mudar_de_pagina
    page.go("/") # Navegação inicial

ft.app(target=main, assets_dir="assets")