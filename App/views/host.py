import flet as ft

def pagina_de_espera_votantes(page: ft.Page, controlador = 'Controlador') -> ft.View:
    conteudo_da_pagina = [
        ft.ElevatedButton("Encerrar espera de votantes", on_click=controlador.encerrar_espera_de_votantes)
    ]
    return ft.View('/espera_votantes', controls=conteudo_da_pagina, vertical_alignment = ft.MainAxisAlignment.CENTER, horizontal_alignment = ft.CrossAxisAlignment.CENTER)

def pagina_de_criacao_de_pauta(page: ft.Page, controlador = 'Controlador') -> ft.View:
    texto = ft.TextField(label='Digite a pauta que será votada')
    
    dropdown_tempo = ft.Dropdown(
        label="Tempo de votação",
        options=[
            ft.dropdown.Option("30"),
            ft.dropdown.Option("45"),
            ft.dropdown.Option("60")
        ],
        value="30"  # valor padrão
    )

    conteudo_da_pagina = [
        ft.Column(
            controls=[
                texto,
                dropdown_tempo,
                ft.ElevatedButton('Enviar pauta', on_click=controlador.enviar_pauta, data=(texto, dropdown_tempo))
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    ]
    return ft.View('/criacao_de_pauta', controls=conteudo_da_pagina,
                   vertical_alignment=ft.MainAxisAlignment.CENTER,
                   horizontal_alignment=ft.CrossAxisAlignment.CENTER)


def pagina_de_espera_votos(page: ft.Page, controlador = 'Controlador') -> ft.View:
    conteudo_da_pagina = [
        ft.ElevatedButton("Encerrar espera por votos", on_click=controlador.encerrar_espera_de_votos)
    ]
    return ft.View('/espera_votos', controls=conteudo_da_pagina, vertical_alignment = ft.MainAxisAlignment.CENTER, horizontal_alignment = ft.CrossAxisAlignment.CENTER)

def pagina_do_resultado(page: ft.Page, resultado: str) -> ft.View:
    conteudo_da_pagina = [
        ft.Text(value=resultado)
    ]
    return ft.View('/resultado', controls=conteudo_da_pagina, vertical_alignment = ft.MainAxisAlignment.CENTER, horizontal_alignment = ft.CrossAxisAlignment.CENTER)
