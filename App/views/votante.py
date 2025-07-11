import flet as ft
from controlador.controller import Controlador


def pagina_de_atencao(pagina: ft.Page, controlador: Controlador) -> ft.View:
    conteudo = [
        ft.Container(height=45, bgcolor="#39746F"),
        ft.Container(
            expand=True,
            content=ft.Column(
                [
                    ft.Text(
                        "ATENÇÃO:",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "PARA QUE NÃO OCORRA\n"
                        "PROBLEMAS EM SEU VOTO,\n"
                        "CERTIFIQUE-SE DE VOTAR E\n"
                        "CONFIRMAR ANTES QUE O\n"
                        "TEMPO DEFINIDO PELO\n"
                        "CRIADOR DA SALA EXPIRE",
                        size=16,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.ElevatedButton(
                        text="CONTINUAR",
                        width=150,
                        height=50,
                        bgcolor="#39746F",
                        color=ft.Colors.WHITE,
                        on_click=controlador.iniciar_escuta_votante,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=40,
            ),
            alignment=ft.alignment.center,
        ),
        ft.Container(height=45, bgcolor="#39746F"),
    ]

    return ft.View(
        route="/atencao_votante",
        controls=conteudo,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.WHITE,
        padding=0,
    )


def pagina_tempo_esgotado(pagina: ft.Page) -> ft.View:
    conteudo = [
        ft.Container(height=45, bgcolor="#39746F"),
        ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column(
                [
                    ft.Icon(name=ft.Icons.TIMER_OFF_OUTLINED, color="#39746F", size=40),
                    ft.Container(
                        content=ft.Text(
                            "Tempo esgotado!\n\nAguarde o resultado da votação.",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                            color=ft.Colors.BLACK,
                        ),
                        padding=ft.padding.only(top=20),
                    ),
                    ft.ProgressRing(color="#39746F"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
                expand=True,
            ),
            bgcolor=ft.Colors.WHITE,
        ),
        ft.Container(height=45, bgcolor="#39746F"),
    ]
    return ft.View(
        "/tempo_esgotado",
        controls=conteudo,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.WHITE,
        padding=0,
    )


def pagina_de_espera(pagina: ft.Page) -> ft.View:
    conteudo_da_pagina = [ft.Text("Por favor Aguarde")]
    return ft.View(
        "/espera",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def aguardar_host(
    pagina: ft.Page,
    mensagem: str = "Por favor, aguarde o\nresponsável pela votação \nliberar a pergunta...",
):
    conteudo = [
        ft.Container(height=45, bgcolor="#39746F"),
        ft.Container(
            expand=True,
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Text(
                            mensagem,
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                            color=ft.Colors.BLACK,
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            bgcolor=ft.Colors.WHITE,
            alignment=ft.alignment.center,
        ),
        ft.Container(height=45, bgcolor="#39746F"),
    ]
    return ft.View(
        "/aguardar_host",
        controls=conteudo,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.WHITE,
        padding=0,
    )


def pagina_de_votacao(pagina: ft.Page, controlador: Controlador) -> ft.View:
    pauta = controlador.mensagem
    mostrador_tempo = ft.Text(
        value=f"Tempo restante: {controlador.tempo_votacao}s",
        size=16,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.RED_500,
    )
    controlador.timer_control_votante = mostrador_tempo
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
                    mostrador_tempo,
                    ft.Container(
                        content=ft.Text(
                            value=pauta,
                            size=14,
                            text_align=ft.TextAlign.CENTER,
                            color=ft.Colors.BLACK,
                        ),
                        padding=20,
                        border=ft.border.all(3, "#39746F"),
                        width=329,
                        height=73,
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
    pagina: ft.Page, controlador: Controlador, voto_selecionado: str
) -> ft.View:
    texto = f"Você confirma seu voto: '{voto_selecionado}'?"

    conteudo = [
        ft.Container(height=45, bgcolor="#39746F"),
        ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column(
                [
                    ft.Text(
                        texto,
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Confirmo",
                                width=140,
                                height=50,
                                bgcolor="#47D147",
                                color=ft.Colors.WHITE,
                                on_click=controlador.confirmar_voto,
                                style=ft.ButtonStyle(
                                    padding=20,
                                    text_style=ft.TextStyle(
                                        size=14,
                                        font_family="Inter",
                                    ),
                                ),
                            ),
                            ft.ElevatedButton(
                                "Não confirmo",
                                width=140,
                                height=50,
                                bgcolor="#C83A3A",
                                color=ft.Colors.WHITE,
                                on_click=controlador.cancelar_voto,
                                style=ft.ButtonStyle(
                                    padding=20,
                                    text_style=ft.TextStyle(
                                        size=14,
                                        font_family="Inter",
                                    ),
                                ),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=40,
                expand=True,
            ),
        ),
        ft.Container(height=45, bgcolor="#39746F"),
    ]

    return ft.View(
        "/confirmacao",
        controls=conteudo,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.WHITE,
        padding=0,
    )


def pagina_do_resultado(pagina: ft.Page, resultado: str) -> ft.View:
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
            shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.GREY),
        )
    ]
    return ft.View(
        "/resultado",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.WHITE,
    )


def pagina_sucesso_voto_computado(pagina: ft.Page) -> ft.View:
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
