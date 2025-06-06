import flet as ft
from controlador.controller import Controlador


def pagina_de_espera(page: ft.Page) -> ft.View:
    conteudo_da_pagina = [ft.Text("Por favor Aguarde")]
    return ft.View(
        "/espera",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def pagina_de_votacao(page: ft.Page, controlador: Controlador) -> ft.View:
    pauta = controlador.mensagem

    conteudo_da_pagina = [
        # Retângulo superior (topo)
        ft.Container(height=45, bgcolor="#39746F"),

        # Container que centraliza o conteúdo no centro da tela
        ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
                controls=[
                    ft.Container(
                        content=ft.Text(
                            value=pauta,
                            size=14,
                            text_align=ft.TextAlign.CENTER,
                            color=ft.Colors.BLACK
                        ),
                        padding=20,
                        border=ft.border.all(3, "#39746F"),
                        width=329,
                        height=73
                    ),
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
                        spacing=20
                    )
                ]
            )
        ),

        # Retângulo inferior (rodapé)
        ft.Container(height=45, bgcolor="#39746F")
    ]

    return ft.View(
        route='/votacao',
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.WHITE,
        padding=0
    )



def pagina_de_confirmacao(
    page: ft.Page, controlador: Controlador, voto_selecionado: str
) -> ft.View:
    texto = f"Você confirma seu voto: '{voto_selecionado}'?"
    conteudo = [
        ft.Text(
            texto, size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER
        ),
        ft.Row(
            [
                ft.ElevatedButton(
                    "Confirmo",
                    bgcolor="#47D147",
                    color=ft.Colors.WHITE,
                    on_click=controlador.confirmar_voto,
                ),
                ft.ElevatedButton(
                    "Não confirmo",
                    bgcolor="#C83A3A",
                    color=ft.Colors.WHITE,
                    on_click=controlador.cancelar_voto,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    ]
    return ft.View(
        "/confirmacao",
        controls=conteudo,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.WHITE,
    )


def pagina_do_resultado(page: ft.Page, resultado: str) -> ft.View:
    conteudo_da_pagina = [
        ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Resultado da Votação",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(value=resultado, size=16, text_align=ft.TextAlign.LEFT),
                ]
            ),
            padding=30,
            width=500,
            bgcolor="#F5F5F5",
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=8, color=ft.colors.GREY),
        )
    ]
    return ft.View(
        "/resultado",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.WHITE,
    )


def pagina_sucesso_voto_computado(page: ft.Page) -> ft.View:
    conteudo = [
        ft.Container(height=45, bgcolor="#39746F"),
        ft.Container(
            expand=True,
            padding=ft.padding.only(top=120, left=40, right=40, bottom=40),
            content=ft.Column(
                [
                    ft.Icon(name=ft.Icons.CHECK, color="#39746F", size=40),
                    ft.Container(
                        content=ft.Text(
                            "Voto computado com sucesso!\n\nAguarde o resultado",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                            color=ft.Colors.BLACK,
                        ),
                        padding=ft.padding.only(top=20),
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=50,
                expand=True,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            alignment=ft.alignment.center,
        ),
        ft.Container(height=45, bgcolor="#39746F"),
    ]
    return ft.View(
        "/sucesso_voto_computado",
        controls=conteudo,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.WHITE,
        padding=0,
    )
