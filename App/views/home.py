import flet as ft
from controlador.controller import Controlador


def pagina_inicial(page: ft.Page, controlador: "Controlador") -> ft.View:
    conteudo_da_pagina = [
        ft.Container(height=45, bgcolor="#39746F"),
        ft.Container(
            expand=True,
            content=ft.Column(
                [
                    ft.Image(src="logo.png", width=200, height=200),
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
                                size=13, weight=ft.FontWeight.NORMAL, font_family="Inter"
                            ),
                        ),
                    ),
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
                                size=13, weight=ft.FontWeight.NORMAL, font_family="Inter"
                            ),
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
        ),
        ft.Container(height=45, bgcolor="#39746F"),
    ]

    return ft.View(
        "/",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.WHITE,
    )


def pagina_do_resultado(page: ft.Page, resultado: str) -> ft.View:
    conteudo_da_pagina = [ft.Text(value=resultado)]
    return ft.View(
        "/resultado",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )