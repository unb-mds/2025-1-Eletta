import flet as ft
from controlador.controller import Controlador


def pagina_de_espera_votantes(page: ft.Page, controlador: Controlador) -> ft.View:
    """
    Página onde o Host aguarda a entrada de novos votantes na sala.
    Agora com o layout padrão da aplicação.
    """
    conteudo_central = ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        content=ft.Column(
            [
                ft.Text(
                    "Aguardando votantes entrarem na sala...",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    color="#39746F",
                ),
                ft.ProgressRing(),
                ft.Container(height=20),
                ft.ElevatedButton(
                    "Encerrar espera e criar pauta",
                    on_click=controlador.encerrar_espera_de_votantes,
                    bgcolor="#39746F",
                    color=ft.Colors.WHITE,
                    width=280,
                    height=50,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=25,
        ),
    )

    return ft.View(
        "/espera_votantes",
        controls=[
            ft.Container(height=45, bgcolor="#39746F"),
            conteudo_central,
            ft.Container(height=45, bgcolor="#39746F"),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.WHITE,
        padding=0,
    )


def pagina_de_criacao_de_pauta(page: ft.Page, controlador: Controlador) -> ft.View:
    pauta = ft.TextField(
        width=300,
        color="#4b7d78",
        label="Defina o tema da votação",
        hint_text="Ex: Você concorda que o preço do RU deve diminuir?",
        label_style=ft.TextStyle(color="#d0d3d9"),
        focused_border_color="#4b7d78",
        border_color="#4b7d78",
    )

    dropdown_tempo = ft.Dropdown(
        label="Defina o tempo de votação (em segundos)",
        width=301,
        options=[
            ft.dropdown.Option("30"),
            ft.dropdown.Option("45"),
            ft.dropdown.Option("60"),
        ],
        value="30",
        color="#4b7d78",
        border_color="#4b7d78",
    )

    conteudo_da_pagina = [
        ft.Container(height=45, bgcolor="#39746F"),
        ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column(
                controls=[
                    pauta,
                    dropdown_tempo,
                    ft.ElevatedButton(
                        text="Gerar votação",
                        width=140,
                        height=56,
                        color=ft.Colors.WHITE,
                        bgcolor="#39746F",
                        data=(pauta, dropdown_tempo),
                        on_click=controlador.enviar_pauta,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=50,
            ),
        ),
        ft.Container(height=45, bgcolor="#39746F"),
    ]

    return ft.View(
        "/criacao_de_pauta",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.WHITE,
        padding=0,
    )


def pagina_de_espera_votos(page: ft.Page, controlador: Controlador) -> ft.View:
    """
    Página onde o Host aguarda o recebimento dos votos.
    Agora com o layout e cores padrão da aplicação.
    """
    conteudo_central = ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        content=ft.Column(
            [
                ft.Text(
                    "Aguardando votos...",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color="#39746F",
                ),
                ft.Text(
                    "A votação encerrará automaticamente.",
                    text_align=ft.TextAlign.CENTER,
                    color="#39746F",
                ),
                ft.ProgressRing(),
                ft.Container(height=20),
                ft.ElevatedButton(
                    "Encerrar Votação Manualmente",
                    on_click=controlador.encerrar_espera_de_votos,
                    bgcolor="#C83A3A",
                    color=ft.Colors.WHITE,
                    width=280,
                    height=50,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=25,
        ),
    )
    return ft.View(
        "/espera_votos",
        controls=[
            ft.Container(height=45, bgcolor="#39746F"),
            conteudo_central,
            ft.Container(height=45, bgcolor="#39746F"),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.WHITE,
        padding=0,
    )


def pagina_do_resultado_host(page: ft.Page, controlador: Controlador) -> ft.View:
    """
    Página de resultado do Host, agora com layout de botões e texto aprimorados.
    """
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
                                controlador.mensagem
                                if controlador.mensagem
                                else "Aguardando resultado..."
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
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                text="Criar nova pauta",
                                width=160,
                                height=50,
                                bgcolor="#39746F",
                                color=ft.Colors.WHITE,
                                on_click=controlador.criar_nova_pauta,
                            ),
                            ft.ElevatedButton(
                                text="Encerrar Sessão",
                                width=160,
                                height=50,
                                bgcolor="#C83A3A",
                                color=ft.Colors.WHITE,
                                on_click=controlador.encerrar_sessao,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=25,
            ),
        ),
        ft.Container(height=45, bgcolor="#39746F"),
    ]

    return ft.View(
        "/resultado_host",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.WHITE,
        padding=0,
    )


def pagina_sucesso_criacao_sala(page: ft.Page) -> ft.View:
    conteudo = [
        ft.Container(height=45, bgcolor="#39746F"),
        ft.Container(
            expand=True,
            padding=ft.padding.only(top=120, left=40, right=40, bottom=40),
            content=ft.Column(
                [
                    ft.Icon(
                        name=ft.icons.CHECK_CIRCLE_OUTLINE,
                        color="#39746F",
                        size=50,
                    ),
                    ft.Container(
                        content=ft.Text(
                            "Sala de votação criada e pauta enviada com sucesso!",
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
                spacing=30,
            ),
            bgcolor=ft.Colors.WHITE,
            alignment=ft.alignment.center,
        ),
        ft.Container(height=45, bgcolor="#39746F"),
    ]
    return ft.View(
        "/sucesso_criacao_sala",
        controls=conteudo,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.WHITE,
        padding=0,
    )