import flet as ft
from controlador.controller import Controlador


def pagina_inicial(pagina: ft.Page, controlador: Controlador) -> ft.View:
    controlador.verificar_status_host()

    botao_votante = ft.ElevatedButton(
        text="Virar Votante",
        width=117,
        height=56,
        color=ft.Colors.WHITE,
        bgcolor="#39746F",
        on_click=controlador.entrar_na_votacao_como_votante,
        disabled=not controlador.host_ativo,
        style=ft.ButtonStyle(
            padding=20,
            text_style=ft.TextStyle(
                size=13,
                weight=ft.FontWeight.NORMAL,
                font_family="Inter",
            ),
        ),
    )

    botao_host = ft.ElevatedButton(
        text="Virar Host",
        width=117,
        height=56,
        color=ft.Colors.WHITE,
        bgcolor="#39746F",
        on_click=controlador.entrar_na_votacao_como_host,
        style=ft.ButtonStyle(
            padding=20,
            text_style=ft.TextStyle(
                size=13,
                weight=ft.FontWeight.NORMAL,
                font_family="Inter",
            ),
        ),
    )

    conteudo_da_pagina = [
        ft.Container(height=45, bgcolor="#39746F"),
        ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column(
                controls=[
                    ft.Image(src="logo.png", width=200, height=200),
                    botao_votante,
                    botao_host,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
            ),
        ),
        ft.Container(height=45, bgcolor="#39746F"),
    ]

    controlador.iniciar_verificacao_periodica_host(botao_votante, pagina)

    return ft.View(
        route="/",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.WHITE,
        padding=0,
    )


def pagina_do_resultado(pagina: ft.Page, resultado: str) -> ft.View:
    resultado_formatado = "\n".join(resultado.split("\n")[1:-2])

    votos = resultado_formatado.strip().split("\n")

    votos_favor = 0.0
    votos_contra = 0.0
    votos_nulos = 0.0

    for voto in votos:
        if "votos a favor" in voto:
            votos_favor = float(voto.split("=")[1].strip().replace("%", ""))
        elif "votos contra" in voto:
            votos_contra = float(voto.split("=")[1].strip().replace("%", ""))
        elif "votos nulos" in voto:
            votos_nulos = float(voto.split("=")[1].strip().replace("%", ""))

    raio_normal = 50
    raio_hover = 60
    estilo_titulo_normal = ft.TextStyle(
        size=13,
        color=ft.Colors.WHITE,
        weight=ft.FontWeight.BOLD,
        shadow=ft.BoxShadow(
            blur_radius=1,
            color=ft.Colors.BLACK,
            spread_radius=0,
            offset=ft.Offset(0, 0),
        ),
    )
    estilo_titulo_hover = ft.TextStyle(
        size=18,
        color=ft.Colors.WHITE,
        weight=ft.FontWeight.BOLD,
        shadow=ft.BoxShadow(
            blur_radius=2,
            color=ft.Colors.BLACK54,
        ),
    )

    def em_evento_grafico(e: ft.PieChartEvent):
        for indice, secao in enumerate(grafico_pizza.sections):
            if indice == e.section_index:
                secao.radius = raio_hover
                secao.title_style = estilo_titulo_hover
            else:
                secao.radius = raio_normal
                secao.title_style = estilo_titulo_normal
        grafico_pizza.update()

    grafico_pizza = ft.PieChart(
        sections=[
            ft.PieChartSection(
                value=votos_favor,
                title=f"{votos_favor:.2f}%",
                color=ft.Colors.GREEN,
                radius=raio_normal,
                title_style=estilo_titulo_normal,
            ),
            ft.PieChartSection(
                value=votos_contra,
                title=f"{votos_contra:.2f}%",
                color=ft.Colors.RED,
                radius=raio_normal,
                title_style=estilo_titulo_normal,
            ),
            ft.PieChartSection(
                value=votos_nulos,
                title=f"{votos_nulos:.2f}%",
                color=ft.Colors.GREY,
                radius=raio_normal,
                title_style=estilo_titulo_normal,
            ),
        ],
        sections_space=0,
        center_space_radius=40,
        on_chart_event=em_evento_grafico,
        expand=True,
    )

    legenda = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
        controls=[
            ft.Row(
                spacing=5,
                controls=[
                    ft.Container(
                        width=12, height=12, bgcolor=ft.Colors.GREEN, border_radius=6
                    ),
                    ft.Text("A favor", size=12, color=ft.Colors.BLACK),
                ],
            ),
            ft.Row(
                spacing=5,
                controls=[
                    ft.Container(
                        width=12, height=12, bgcolor=ft.Colors.RED, border_radius=6
                    ),
                    ft.Text("Contra", size=12, color=ft.Colors.BLACK),
                ],
            ),
            ft.Row(
                spacing=5,
                controls=[
                    ft.Container(
                        width=12, height=12, bgcolor=ft.Colors.GREY, border_radius=6
                    ),
                    ft.Text("Abstenções", size=12, color=ft.Colors.BLACK),
                ],
            ),
        ],
    )

    conteudo_da_pagina = [
        ft.Container(height=45, bgcolor="#39746F"),
        ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Resultado da Votação",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color="#39746F",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    grafico_pizza,
                    legenda,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
            ),
        ),
        ft.Container(height=45, bgcolor="#39746F"),
    ]

    return ft.View(
        "/resultado",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.WHITE,
        padding=0,
    )