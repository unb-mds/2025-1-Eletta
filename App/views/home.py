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
        ft.Container(height=45, bgcolor="#39746F"),
        ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column(
                [
                    ft.Text(
                        "Resultado da Votação",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color="#39746F",
                    ),
                    ft.Container(
                        content=ft.Text(
                            value=(
                                resultado if resultado else "Aguardando resultado..."
                            ),
                            selectable=True,
                            text_align=ft.TextAlign.LEFT,
                            color=ft.Colors.BLACK,
                            size=14,
                            font_family="Monospace",
                        ),
                        padding=20,
                        border=ft.border.all(2, "#39746F"),
                        border_radius=ft.border_radius.all(10),
                        width=350,
                        alignment=ft.alignment.center,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=25,
                scroll=ft.ScrollMode.AUTO,
            ),
        ),
        ft.Container(height=45, bgcolor="#39746F"),
    ]
    return ft.View(
        "/resultado",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.colors.WHITE,
        padding=0,
    )
