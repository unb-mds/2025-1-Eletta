import flet as ft
from controlador.controller import Controlador


def pagina_de_espera_votantes(page: ft.Page, controlador: Controlador) -> ft.View:
    conteudo_da_pagina = [
        # Retângulo superior
        ft.Container(height=45, bgcolor="#39746F"),
        # Conteúdo central com centralização total
        ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column(
                [
                    ft.Text(
                        "Aguardando votantes...",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.ElevatedButton(
                        text="Prosseguir para votação",
                        width=240,
                        height=50,
                        bgcolor="#39746F",
                        color=ft.Colors.WHITE,
                        on_click=controlador.encerrar_espera_de_votantes,
                        style=ft.ButtonStyle(
                            padding=20,
                            text_style=ft.TextStyle(
                                size=14,
                                weight=ft.FontWeight.NORMAL,
                                font_family="Inter",
                            ),
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
                spacing=30,
            ),
        ),
        # Retângulo inferior
        ft.Container(height=45, bgcolor="#39746F"),
    ]

    return ft.View(
        "/espera_votantes",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.WHITE,
        padding=0,
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

    dropdown_tempo = ft.Dropdown(
        label="Defina o tempo (segundos)",
        hint_text="30",
        options=[
            ft.dropdown.Option(
                key="30",
                text="00:30",
                content=ft.ListTile(
                    title=ft.Text("00:30", text_align=ft.TextAlign.CENTER),
                    dense=True,
                ),
            ),
            ft.dropdown.Option(
                key="45",
                text="00:45",
                content=ft.ListTile(
                    title=ft.Text("00:45", text_align=ft.TextAlign.CENTER),
                    dense=True,
                ),
            ),
            ft.dropdown.Option(
                key="60",
                text="01:00",
                content=ft.ListTile(
                    title=ft.Text("01:00", text_align=ft.TextAlign.CENTER),
                    dense=True,
                ),
            ),
        ],
        value="30",
        color="#4b7d78",
        border_color="#4b7d78",
        text_align=ft.TextAlign.CENTER,  # Centraliza o texto selecionado
        content_padding=ft.padding.only(left=40),  # Ajuste o valor conforme necessário
        width=301,  # Largura fixa para melhor controle
    )

    conteudo_da_pagina = [
        ft.Container(height=45, bgcolor="#39746F"),
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=dropdown_tempo,
                        # Centraliza o Container que envolve o Dropdown
                        alignment=ft.alignment.center,
                        width=300,  # Opcional: define um limite de largura
                    ),
                    pauta,
                    ft.ElevatedButton(
                        text="Gerar votação",
                        width=140,
                        height=56,
                        color=ft.Colors.WHITE,
                        bgcolor="#39746F",
                        data=(pauta, dropdown_tempo),
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
            alignment=ft.alignment.center,  # Centraliza a Column no Container
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
    conteudo_da_pagina = [
        # Retângulo superior
        ft.Container(height=45, bgcolor="#39746F"),
        # Conteúdo central com centralização total
        ft.Container(
            expand=True,
            content=ft.Column(
                [
                    ft.Text(
                        "Aguardando votos...",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.ElevatedButton(
                        text="Encerrar votação",
                        width=240,
                        height=50,
                        bgcolor="#39746F",
                        color=ft.Colors.WHITE,
                        on_click=controlador.encerrar_espera_de_votos,
                        style=ft.ButtonStyle(
                            padding=20,
                            text_style=ft.TextStyle(
                                size=14,
                                weight=ft.FontWeight.NORMAL,
                                font_family="Inter",
                            ),
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # vertical
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # horizontal
                expand=True,
                spacing=30,  # permite ocupar o Container pai
            ),
            alignment=ft.alignment.center,  # centraliza a Column no Container
        ),
        # Retângulo inferior
        ft.Container(height=45, bgcolor="#39746F"),
    ]

    return ft.View(
        "/espera_votos",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.WHITE,
        padding=0,
    )


def pagina_do_resultado(page: ft.Page, resultado: str) -> ft.View:
    conteudo_da_pagina = [ft.Text(value=resultado)]
    return ft.View(
        "/resultado",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def pagina_do_resultado_host_intermediario(
    page: ft.Page, controlador: Controlador
) -> ft.View:
    """
    Tela que mostra o resultado apenas para o host com um gráfico de pizza e legenda.
    """
    resultado_formatado = "\n".join(controlador.resultado_votacao.split("\n")[1:-2])

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

    normal_radius = 50
    hover_radius = 60
    normal_title_style = ft.TextStyle(
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
    hover_title_style = ft.TextStyle(
        size=18,
        color=ft.Colors.WHITE,
        weight=ft.FontWeight.BOLD,
        shadow=ft.BoxShadow(
            blur_radius=2,
            color=ft.Colors.BLACK54,
        ),
    )

    def on_chart_event(e: ft.PieChartEvent):
        for idx, section in enumerate(chart.sections):
            if idx == e.section_index:
                section.radius = hover_radius
                section.title_style = hover_title_style
            else:
                section.radius = normal_radius
                section.title_style = normal_title_style
        chart.update()

    chart = ft.PieChart(
        sections=[
            ft.PieChartSection(
                value=votos_favor,
                title=f"{votos_favor:.2f}%",
                color=ft.Colors.GREEN,
                radius=normal_radius,
                title_style=normal_title_style,
            ),
            ft.PieChartSection(
                value=votos_contra,
                title=f"{votos_contra:.2f}%",
                color=ft.Colors.RED,
                radius=normal_radius,
                title_style=normal_title_style,
            ),
            ft.PieChartSection(
                value=votos_nulos,
                title=f"{votos_nulos:.2f}%",
                color=ft.Colors.GREY,
                radius=normal_radius,
                title_style=normal_title_style,
            ),
        ],
        sections_space=0,
        center_space_radius=40,
        on_chart_event=on_chart_event,
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
                [
                    ft.Text(
                        "Resultado da votação:",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK,
                    ),
                    chart,
                    legenda,
                    ft.ElevatedButton(
                        text="Enviar resultado",
                        width=200,
                        height=50,
                        bgcolor="#39746F",
                        color=ft.Colors.WHITE,
                        on_click=controlador.enviar_resultado_para_votantes,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
            ),
        ),
        ft.Container(height=45, bgcolor="#39746F"),
    ]

    return ft.View(
        "/resultado_host_intermediario",
        controls=conteudo_da_pagina,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.WHITE,
        padding=0,
    )


def pagina_do_resultado_host_final(page: ft.Page, controlador: Controlador) -> ft.View:
    """
    Tela final do host, que aparece após o resultado ser enviado.
    Agora mostra um gráfico de pizza com legenda.
    """
    # Extrai os valores percentuais do resultado já calculado
    resultado_formatado = "\n".join(controlador.resultado_votacao.split("\n")[1:-2])

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

    normal_radius = 50
    hover_radius = 60
    normal_title_style = ft.TextStyle(
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
    hover_title_style = ft.TextStyle(
        size=18,
        color=ft.Colors.WHITE,
        weight=ft.FontWeight.BOLD,
        shadow=ft.BoxShadow(
            blur_radius=2,
            color=ft.Colors.BLACK54,
        ),
    )

    def on_chart_event(e: ft.PieChartEvent):
        for idx, section in enumerate(chart.sections):
            if idx == e.section_index:
                section.radius = hover_radius
                section.title_style = hover_title_style
            else:
                section.radius = normal_radius
                section.title_style = normal_title_style
        chart.update()

    chart = ft.PieChart(
        sections=[
            ft.PieChartSection(
                value=votos_favor,
                title=f"{votos_favor:.2f}%",
                color=ft.Colors.GREEN,
                radius=normal_radius,
                title_style=normal_title_style,
            ),
            ft.PieChartSection(
                value=votos_contra,
                title=f"{votos_contra:.2f}%",
                color=ft.Colors.RED,
                radius=normal_radius,
                title_style=normal_title_style,
            ),
            ft.PieChartSection(
                value=votos_nulos,
                title=f"{votos_nulos:.2f}%",
                color=ft.Colors.GREY,
                radius=normal_radius,
                title_style=normal_title_style,
            ),
        ],
        sections_space=0,
        center_space_radius=40,
        on_chart_event=on_chart_event,
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
                [
                    ft.Text(
                        "Resultado da votação final:",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color="#000000",
                    ),
                    chart,
                    legenda,
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
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
            ),
        ),
        ft.Container(height=45, bgcolor="#39746F"),
    ]

    return ft.View(
        "/resultado_host_final",
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
                    ft.Icon(name=ft.Icons.CHECK, color="#39746F", size=40),
                    ft.Container(
                        content=ft.Text(
                            "Sala de votação criada com sucesso!",
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
        "/sucesso_criacao_sala",
        controls=conteudo,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.WHITE,
        padding=0,
    )
