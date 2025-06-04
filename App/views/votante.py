import flet as ft
from controlador.controller import Controlador


def pagina_de_espera(page: ft.Page) -> ft.View:
    conteudo_da_pagina = [ft.Text("Por favor Aguarde...")]
    return ft.View(
        "/espera",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def pagina_de_votacao(page: ft.Page, controlador: "Controlador") -> ft.View:
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
        color=ft.colors.RED_500,
    )
    controlador.timer_control_votante = timer_display

    conteudo_da_pagina = [
        timer_display,
        ft.Container(height=10),
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
        ft.Container(height=20),
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
    ]
    return ft.View(
        "/votacao",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.colors.WHITE,
    )


def pagina_de_confirmacao(
    page: ft.Page, controlador: "Controlador", voto_selecionado: str
) -> ft.View:
    texto = f"Você confirma seu voto: '{voto_selecionado}'?"
    conteudo = [
        ft.Text(texto, size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
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
    ]
    return ft.View(
        "/confirmacao",
        controls=conteudo,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.colors.WHITE,
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
                    ft.Markdown(
                        value=f"```\n{resultado}\n```"
                        if resultado
                        else "Aguardando resultado...",
                        selectable=True,
                        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                        code_theme="atom-one-dark",
                    ),
                    ft.ElevatedButton(
                        "Voltar ao Início",
                        on_click=lambda _: page.go("/"),
                        bgcolor="#39746F",
                        color=ft.colors.WHITE,
                    ),
                ],
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=30,
            width=500,
            bgcolor="#F5F5F5",
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=8, color=ft.colors.GREY),
            alignment=ft.alignment.center,
        )
    ]
    return ft.View(
        "/resultado",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.colors.WHITE,
    )