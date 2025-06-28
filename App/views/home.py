import flet as ft
from controlador.controller import Controlador


def pagina_inicial(page: ft.Page, controlador: Controlador) -> ft.View:
    # Verifica o status do host ao carregar a página
    controlador.verificar_status_host()

    # Botão de votante
    botao_votante = ft.ElevatedButton(
        text="virar votante",
        width=117,
        height=56,
        color=ft.Colors.WHITE,
        bgcolor="#39746F",
        on_click=controlador.entrar_na_votacao_como_votante,
        disabled=not controlador.host_ativo,  # Desabilitado se não houver host ativo
        style=ft.ButtonStyle(
            padding=20,
            text_style=ft.TextStyle(
                size=13,
                weight=ft.FontWeight.NORMAL,
                font_family="Inter",
            ),
        ),
    )

    # Botão de host
    botao_host = ft.ElevatedButton(
        text="virar host",
        width=117,
        height=56,
        color=ft.Colors.WHITE,
        bgcolor="#39746F",
        on_click=controlador.entrar_na_votacao_como_host,
        style=ft.ButtonStyle(
            padding=20,
            text_style=ft.TextStyle(
                size=13,
                weight=ft.FontWeight.NORMAL,
                font_family="Inter",
            ),
        ),
    )

    conteudo_da_pagina = [
        # Retângulo superior (topo)
        ft.Container(height=45, bgcolor="#39746F"),
        # Container central com conteúdo centralizado verticalmente
        ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column(
                controls=[
                    ft.Image(src="logo.png", width=200, height=200),
                    botao_votante,
                    botao_host,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
            ),
        ),
        # Retângulo inferior (rodapé)
        ft.Container(height=45, bgcolor="#39746F"),
    ]

    controlador.iniciar_verificacao_periodica_host(botao_votante, page)

    return ft.View(
        route="/",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.WHITE,
        padding=0,
    )


def pagina_do_resultado(page: ft.Page, resultado: str) -> ft.View:
    conteudo_da_pagina = [
        # Retângulo superior
        ft.Container(height=45, bgcolor="#39746F"),
        # Conteúdo central
        ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Resultado da Votação",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color="#39746F",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        value=resultado,
                        size=16,
                        color=ft.Colors.BLACK,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
            ),
        ),
        # Retângulo inferior
        ft.Container(height=45, bgcolor="#39746F"),
    ]

    return ft.View(
        "/resultado",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.WHITE,
        padding=0,
    )
