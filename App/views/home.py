import flet as ft
from controlador import controller


def pagina_inicial(page: ft.Page, controlador: controller) -> ft.View:
    conteudo_da_pagina = [
        ft.Column(
            [
                ft.ElevatedButton(
                    text="virar votante",
                    width=117,
                    height=56,
                    color=ft.colors.WHITE,
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
                    color=ft.colors.WHITE,
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
        )
    ]
    return ft.View(
        "/",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.colors.WHITE,
    )


def pagina_do_resultado(page: ft.Page, resultado: str) -> ft.View:
    conteudo_da_pagina = [ft.Text(value=resultado)]
    return ft.View(
        "/resultado",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
