import flet as ft
from controlador.controller import Controlador


def pagina_inicial(page: ft.Page, controlador: Controlador) -> ft.View:
    # Verifica o status do host ao carregar a página
    controlador.verificar_status_host()

    # Botão de votante
    botao_votante = ft.ElevatedButton(
        text="virar votante",
        width=117,
        height=56,
        color=ft.Colors.WHITE,
        bgcolor="#39746F",
        on_click=controlador.entrar_na_votacao_como_votante,
        disabled=not controlador.host_ativo,  # Desabilitado se não houver host ativo
        style=ft.ButtonStyle(
            padding=20,
            text_style=ft.TextStyle(
                size=13,
                weight=ft.FontWeight.NORMAL,
                font_family="Inter",
            ),
        ),
    )

    # Botão de host
    botao_host = ft.ElevatedButton(
        text="virar host",
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
        # Retângulo superior (topo)
        ft.Container(height=45, bgcolor="#39746F"),
        # Container central com conteúdo centralizado verticalmente
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
        # Retângulo inferior (rodapé)
        ft.Container(height=45, bgcolor="#39746F"),
    ]

    controlador.iniciar_verificacao_periodica_host(botao_votante, page)

    return ft.View(
        route="/",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.WHITE,
        padding=0,
    )


def pagina_do_resultado(page: ft.Page, resultado: str) -> ft.View:
    partes = resultado.strip().split()
    votos_a_favor = int(partes[0])
    votos_contra = int(partes[1])
    votos_abstencao = int(partes[2])

    grafico = ft.BarChart(
        bar_groups=[
            ft.BarChartGroup(
                x=0,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=votos_a_favor,
                        width=40,
                        color=ft.Colors.GREEN,
                        border_radius=1,
                    ),
                ],
            ),
            ft.BarChartGroup(
                x=1,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=votos_contra,
                        width=40,
                        color=ft.Colors.RED,
                        border_radius=1,
                    ),
                ],
            ),
            ft.BarChartGroup(
                x=2,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=votos_abstencao,
                        width=40,
                        color=ft.Colors.GREY,
                        border_radius=1,
                    ),
                ],
            ),
        ],
        border=ft.border.all(1, "#39746F"),
        left_axis=ft.ChartAxis(
            labels_size=40,
            title=ft.Text("Votos", color="#39746F"),
            title_size=50,
            labels=[
                ft.ChartAxisLabel(value=i, label=ft.Text(str(i), color="#39746F"))
                for i in range(0, 51, 10)
            ],
        ),
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=0,
                    label=ft.Container(ft.Text("A favor", color="#39746F"), padding=10),
                ),
                ft.ChartAxisLabel(
                    value=1,
                    label=ft.Container(ft.Text("Contra", color="#39746F"), padding=10),
                ),
                ft.ChartAxisLabel(
                    value=2,
                    label=ft.Container(
                        ft.Text("Abstenções", color="#39746F"), padding=10
                    ),
                ),
            ],
            labels_size=40,
        ),
        horizontal_grid_lines=ft.ChartGridLines(
            color="#39746F", width=1, dash_pattern=[3, 3]
        ),
        tooltip_bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.GREY_300),
        max_y=50,
        interactive=True,
        expand=True,
    )

    conteudo_da_pagina = [
        # Retângulo superior
        ft.Container(height=45, bgcolor="#39746F"),
        # Conteúdo central
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
                    ft.Container(
                        content=grafico,
                        alignment=ft.alignment.center,
                        padding=20,
                        width=600,
                        margin=ft.margin.only(right=20),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
            ),
        ),
        # Retângulo inferior
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
