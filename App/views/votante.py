import flet as ft
from controlador.controller import Controlador

def pagina_de_espera(page: ft.Page) -> ft.View:
    conteudo_da_pagina = [
        ft.Text("Por favor Aguarde...") # Adicionado reticências
    ]
    return ft.View('/espera', controls=conteudo_da_pagina, vertical_alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

def pagina_de_votacao(page: ft.Page, controlador: 'Controlador') -> ft.View:
    pauta = controlador.mensagem
    # Tempo inicial para exibição antes que a thread do cronômetro o atualize
    initial_time_display = f"Tempo restante: {controlador.tempo_votacao}s" if controlador.tempo_votacao > 0 else "Aguardando início do tempo..."

    # Cria o controle ft.Text para exibição do cronômetro
    timer_display = ft.Text(
        value=initial_time_display,
        size=16,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
       color=ft.colors.RED_500 # Cor do texto do cronômetro
    )
    # Passa este controle para o controlador para que ele possa atualizá-lo
    controlador.timer_control_votante = timer_display

    conteudo_da_pagina = [
        timer_display, # Adicionado exibição do cronômetro aqui
        ft.Container(height=10), # Espaçador
        ft.Container(
            content=ft.Text(
                value=pauta if pauta else "Aguardando pauta...", # Lida se pauta for None inicialmente
                size=14,
                text_align=ft.TextAlign.CENTER,
                color=ft.Colors.BLACK
            ),
            padding=20,
            border=ft.border.all(3, "#39746F"),
            width=329,
            height=73,
            alignment=ft.alignment.center
        ),
        ft.Container(height=20), # Espaçador
        ft.Column(
            controls=[
                ft.ElevatedButton(
                    text='A favor',
                    width=117,
                    height=56,
                    bgcolor='#47D147',
                    color=ft.Colors.WHITE,
                    on_click=controlador.votar,
                    data=2
                ),
                ft.ElevatedButton(
                    text='Contra',
                    width=117,
                    height=56,
                    bgcolor='#C83A3A',
                    color=ft.Colors.WHITE,
                    on_click=controlador.votar,
                    data=1
                ),
                ft.ElevatedButton(
                    text='Abster-se',
                    width=117,
                    height=56,
                    bgcolor='#828E82',
                    color=ft.Colors.WHITE,
                    on_click=controlador.votar,
                    data=0
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Garante que a coluna em si esteja centralizada se não estiver expandindo
            spacing=20
        )
    ]
    return ft.View(
        '/votacao',
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.colors.WHITE
    )

def pagina_de_confirmacao(page: ft.Page, controlador: 'Controlador', voto_selecionado: str) -> ft.View:
    texto = f"Você confirma seu voto: '{voto_selecionado}'?"
    conteudo = [
        ft.Text(texto, size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        ft.Container(height=20), # Espaçador
        ft.Row(
            [
                ft.ElevatedButton("Confirmo", bgcolor="#47D147", color=ft.Colors.WHITE, on_click=controlador.confirmar_voto, width=120, height=50),
                ft.ElevatedButton("Não confirmo", bgcolor="#C83A3A", color=ft.Colors.WHITE, on_click=controlador.cancelar_voto, width=120, height=50),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )
    ]
    return ft.View(
        "/confirmacao",
        controls=conteudo,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.colors.WHITE
    )

def pagina_do_resultado(page: ft.Page, resultado: str) -> ft.View: # Página de resultado do votante
    conteudo_da_pagina = [
        ft.Container(
            content=ft.Column([
                ft.Text("Resultado da Votação", size=22, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Markdown( # Usa Markdown para resultados potencialmente multilinha
                    value=f"```\n{resultado}\n```" if resultado else "Aguardando resultado...", # Exibe a string bruta em um bloco de código
                    selectable=True,
                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB, # Conjunto de extensões Markdown
                    code_theme="atom-one-dark", # Opcional: para melhor estilização do bloco de código
                ),
                 ft.ElevatedButton(
                    "Voltar ao Início",
                    on_click=lambda _: page.go("/"),
                    bgcolor="#39746F",
                    color=ft.colors.WHITE
                )
            ], scroll=ft.ScrollMode.AUTO), # Torna a coluna rolável se o conteúdo for grande
            padding=30,
            width=500,
            # height=400, # Opcional: define uma altura fixa
            bgcolor="#F5F5F5",
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=8, color=ft.colors.GREY),
            alignment=ft.alignment.center
        )
    ]
    return ft.View(
        '/resultado', # Esta rota é usada por Eletta.py para home.pagina_do_resultado.
                      # Garanta a consistência se esta função for ser usada.
                      # Eletta.py atualmente chama home.pagina_do_resultado.
                      # Se esta deve ser usada para votantes, Eletta.py precisa apontar para ela.
                      # Por enquanto, vamos assumir que `home.pagina_do_resultado` é a principal para o fluxo geral.
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.colors.WHITE
    )