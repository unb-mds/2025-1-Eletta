import flet as ft


def pagina_de_espera_votantes(page: ft.Page, controlador="Controlador") -> ft.View:
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


def pagina_de_criacao_de_pauta(page: ft.Page, controlador="Controlador") -> ft.View:
    texto = ft.TextField(label="digite a pauta que será votada")
    conteudo_da_pagina = [
        ft.Row(
            [
                texto,
                ft.ElevatedButton(
                    "enviar pauta", on_click=controlador.enviar_pauta, data=texto
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    ]
    return ft.View(
        "/criacao_de_pauta",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def pagina_de_espera_votos(page: ft.Page, controlador="Controlador") -> ft.View:
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


def pagina_do_resultado_host(page: ft.Page, controlador: "Controlador") -> ft.View:
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
