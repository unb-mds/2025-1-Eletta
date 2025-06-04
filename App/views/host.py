import flet as ft
from controlador.controller import Controlador


def pagina_de_espera_votantes(page: ft.Page, controlador: Controlador) -> ft.View:
    conteudo_da_pagina = [
        ft.ElevatedButton(
            "Encerrar espera de votantes",
            on_click=controlador.encerrar_espera_de_votantes,
        )
    ]
    return ft.View(
        "/espera_votantes",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def pagina_de_criacao_de_pauta(page: ft.Page, controlador: Controlador) -> ft.View:
    pauta = ft.TextField(  # Armazena a pauta
        width=300,
        color="#4b7d78",
        label="Defina o tema da votação",
        hint_text="Ex: Você concorda que o preço do RU deve diminuir?",
        label_style=ft.TextStyle(color="#d0d3d9"),
        focused_border_color="#4b7d78",
        border_color="#4b7d78",
    )
    conteudo_da_pagina = [
        ft.Container(height=45, bgcolor="#39746F"),
        # Container que centraliza a coluna na tela
        ft.Container(
            content=ft.Column(  # Coluna com os conteudos da pagina
                controls=[
                    ft.Dropdown(  # Seleção do tempo
                        label="Defina o tempo",
                        width=301,
                        hint_text="00:30",
                        options=[
                            ft.dropdown.Option(
                                key="00:30",
                                content=ft.Text(value="00:30", color="#4b7d78"),
                            ),  # Opções
                            ft.dropdown.Option(
                                key="00:45",
                                content=ft.Text(value="00:45", color="#4b7d78"),
                            ),
                            ft.dropdown.Option(
                                key="01:00",
                                content=ft.Text(value="01:00", color="#4b7d78"),
                            ),
                        ],
                        color="#4b7d78",
                        border_color="#4b7d78",
                        bgcolor=ft.Colors.WHITE,
                    ),
                    pauta,
                    ft.ElevatedButton(  # Botão de iniciar a votação
                        text="Gerar votação",
                        width=140,
                        height=56,
                        color=ft.Colors.WHITE,
                        bgcolor="#39746F",
                        data=pauta,
                        on_click=controlador.enviar_pauta,
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
                spacing=70,
            ),
            expand=True,
            alignment=ft.alignment.center,  # centraliza a coluna dentro do container
        ),
        ft.Container(height=45, bgcolor="#39746F"),
    ]

    return ft.View(
        "/criacao_de_pauta",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.colors.WHITE,
        padding=0,
    )


def pagina_de_espera_votos(page: ft.Page, controlador: Controlador) -> ft.View:
    conteudo_da_pagina = [
        ft.ElevatedButton(
            "Encerrar espera por votos", on_click=controlador.encerrar_espera_de_votos
        )
    ]
    return ft.View(
        "/espera_votos",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def pagina_do_resultado(page: ft.Page, resultado: str) -> ft.View:
    conteudo_da_pagina = [ft.Text(value=resultado)]
    return ft.View(
        "/resultado",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def pagina_do_resultado_host(page: ft.Page, controlador: Controlador) -> ft.View:
    conteudo_da_pagina = [
        ft.Column(
            [
                ft.Text(controlador.mensagem),
                ft.ElevatedButton(
                    "criar nova pauta", on_click=controlador.criar_nova_pauta
                ),
                ft.ElevatedButton(
                    "Encerrar Sessão", on_click=controlador.encerrar_sessao
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    ]
    return ft.View(
        "/resultado_host",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
