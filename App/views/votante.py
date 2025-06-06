import flet as ft
from controlador.controller import Controlador


def pagina_de_espera(page: ft.Page) -> ft.View:
    """
    Página onde o Votante aguarda o Host iniciar uma votação.
    Agora com o layout padrão da aplicação.
    """
    conteudo_central = ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        content=ft.Column(
            [
                ft.Text(
                    "Por favor, aguarde o Host iniciar a votação...",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    color="#39746F",
                ),
                ft.Container(height=20),
                ft.ProgressRing(),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=25,
        ),
    )

    return ft.View(
        "/espera",
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


def pagina_de_votacao(page: ft.Page, controlador: Controlador) -> ft.View:
    pauta = controlador.mensagem
    initial_time_display = (
        f"Tempo restante: {controlador.tempo_votacao}s"
        if controlador.tempo_votacao > 0
        else "Aguardando início do tempo..."
    )

    timer_display = ft.Text(
        value=initial_time_display,
        size=16,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
        color=ft.Colors.RED_500,
    )
    controlador.timer_control_votante = timer_display

    conteudo_da_pagina = [
        ft.Container(height=45, bgcolor="#39746F"),
        ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
                controls=[
                    timer_display,
                    ft.Container(
                        content=ft.Text(
                            value=pauta if pauta else "Aguardando pauta...",
                            size=14,
                            text_align=ft.TextAlign.CENTER,
                            color=ft.Colors.BLACK,
                        ),
                        padding=20,
                        border=ft.border.all(3, "#39746F"),
                        width=329,
                        height=73,
                        alignment=ft.alignment.center,
                    ),
                    ft.Column(
                        controls=[
                            ft.ElevatedButton(
                                text="A favor",
                                width=117,
                                height=56,
                                bgcolor="#47D147",
                                color=ft.Colors.WHITE,
                                on_click=controlador.votar,
                                data=2,
                            ),
                            ft.ElevatedButton(
                                text="Contra",
                                width=117,
                                height=56,
                                bgcolor="#C83A3A",
                                color=ft.Colors.WHITE,
                                on_click=controlador.votar,
                                data=1,
                            ),
                            ft.ElevatedButton(
                                text="Abster-se",
                                width=117,
                                height=56,
                                bgcolor="#828E82",
                                color=ft.Colors.WHITE,
                                on_click=controlador.votar,
                                data=0,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                    ),
                ],
            ),
        ),
        ft.Container(height=45, bgcolor="#39746F"),
    ]
    return ft.View(
        route="/votacao",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.WHITE,
        padding=0,
    )


def pagina_de_confirmacao(
    page: ft.Page, controlador: Controlador, voto_selecionado: str
) -> ft.View:
    texto = f"Você confirma seu voto: '{voto_selecionado}'?"

    conteudo_central = ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        content=ft.Column(
            [
                ft.Text(
                    texto,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    color="#39746F",
                ),
                ft.Container(height=20),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Confirmo",
                            bgcolor="#47D147",
                            color=ft.Colors.WHITE,
                            on_click=controlador.confirmar_voto,
                            width=120,
                            height=50,
                        ),
                        ft.ElevatedButton(
                            "Não confirmo",
                            bgcolor="#C83A3A",
                            color=ft.Colors.WHITE,
                            on_click=controlador.cancelar_voto,
                            width=120,
                            height=50,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    return ft.View(
        "/confirmacao",
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


def pagina_sucesso_voto_computado(page: ft.Page) -> ft.View:
    conteudo = [
        ft.Container(height=45, bgcolor="#39746F"),
        ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column(
                [
                    ft.Icon(
                        name=ft.icons.CHECK_CIRCLE_OUTLINE, color="#39746F", size=50
                    ),
                    ft.Container(
                        content=ft.Text(
                            "Voto computado com sucesso!\n\nAguarde o resultado.",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                            color=ft.Colors.BLACK,
                        ),
                        padding=ft.padding.only(top=20),
                    ),
                    ft.ProgressRing(),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
            ),
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
