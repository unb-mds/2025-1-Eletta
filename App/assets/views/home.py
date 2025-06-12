import flet as ft
from controlador.controller import Controlador


def pagina_inicial(page: ft.Page, controlador: Controlador) -> ft.View:
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
                    # Botão de votante
                    ft.ElevatedButton(
                        text="virar votante",
                        width=117,
                        height=56,
                        color=ft.Colors.WHITE,
                        bgcolor="#39746F",
                        on_click=controlador.entrar_na_votacao_como_votante,
                        style=ft.ButtonStyle(
                            padding=20,
                            text_style=ft.TextStyle(
                                size=13,
                                weight=ft.FontWeight.NORMAL,
                                font_family="Inter",
                            ),
                        ),
                    ),
                    # Botão de host
                    ft.ElevatedButton(
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
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
            ),
        ),
        # Retângulo inferior (rodapé)
        ft.Container(height=45, bgcolor="#39746F"),
    ]

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
