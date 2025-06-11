import flet as ft
from socket import socket
from threading import Thread, Event
from servidor import servidor, cliente
from servidor.Data_Base.DB import Banco_de_Dados
import time


class Controlador:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Elleta"
        self.udp_socket: socket
        self.banco_de_dados: Banco_de_Dados
        self.mensagem: str
        self.process: Thread
        self.flag_controle: Event
        self.voto_pendente: str
        self.page.go("/")

    # ----------- votante -------------
    def entrar_na_votacao_como_votante(self, e: ft.ControlEvent) -> None:
        """
        Inicia a conexão do votante e o redireciona para a tela de atenção.
        """
        self.udp_socket = cliente.virar_votante()
        self.page.go("/atencao_votante")

    def iniciar_escuta_votante(self, e: ft.ControlEvent) -> None:
        """
        Inicia a escuta por pautas após o votante clicar em 'Continuar'.
        """
        self.page.go("/aguardar_host")
        # A lógica de receber a pauta e navegar para a votação continua a mesma
        pauta = cliente.receber_mensagem(self.udp_socket)
        while pauta is None or pauta == "":
            self.page.go("/aguardar_host")
            pauta = cliente.receber_mensagem(self.udp_socket)

        self.mensagem = pauta
        if self.mensagem != "votação encerrada":
            self.page.go("/votacao")

    def votar(self, e: ft.ControlEvent) -> None:
        if e.control.data == 2:
            self.voto_pendente = "a favor"
        elif e.control.data == 1:
            self.voto_pendente = "contra"
        elif e.control.data == 0:
            self.voto_pendente = "nulo"
        self.page.go("/confirmacao")

    def confirmar_voto(self, e: ft.ControlEvent) -> None:
        cliente.votar(self.udp_socket, self.voto_pendente, self.mensagem)
        cliente.votar(self.udp_socket, self.voto_pendente, self.mensagem)
        self.page.go("/sucesso_voto_computado")
        self.mensagem = cliente.receber_mensagem(self.udp_socket)
        self.page.go("/resultado")
        time.sleep(
            10
        )  # Aguarda, pelo menos, 10 segundos para o votante interpretar o resultado antes de receber uma nova pauta ou encerrar a sessão
        print("aguardando host")
        self.mensagem = cliente.receber_mensagem(self.udp_socket)
        print(f"mensagem recebida: {self.mensagem}")
        if self.mensagem == "sessao encerrada":
            self.page.go("/")
        elif self.mensagem == "aguardando nova pauta":
            self.page.go("/aguardar_host")
            self.mensagem = cliente.receber_mensagem(self.udp_socket)
            while self.mensagem == "" or self.mensagem is None:
                self.mensagem = cliente.receber_mensagem(self.udp_socket)
            self.page.go("/votacao")

    def cancelar_voto(self, e: ft.ControlEvent) -> None:
        nova_mensagem = cliente.receber_mensagem(self.udp_socket)
        if nova_mensagem == "votação encerrada":
            self.mensagem = nova_mensagem
            self.page.go("/resultado")
        else:
            self.page.go("/votacao")

    # ----------- host -------------
    def entrar_na_votacao_como_host(self, e: ft.ControlEvent) -> None:
        self.udp_socket = servidor.virar_host()
        self.banco_de_dados, self.process, self.flag_de_controle = (
            servidor.aguardar_votantes(self.udp_socket)
        )
        self.page.go("/espera_votantes")

    def encerrar_espera_de_votantes(self, e: ft.ControlEvent) -> None:
        self.flag_de_controle.set()
        self.process.join()
        self.page.go("/criacao_de_pauta")

    def enviar_pauta(self, e: ft.ControlEvent) -> None:
        self.process, self.flag_de_controle = servidor.aguardar_votos(
            self.banco_de_dados, self.udp_socket
        )
        self.mensagem = e.control.data.value
        self.banco_de_dados.adicionar_pauta(self.mensagem)
        self.banco_de_dados.serializar_dados()
        servidor.mandar_mensagem(self.banco_de_dados, self.udp_socket, self.mensagem)
        self.page.go("/sucesso_criacao_sala")
        time.sleep(5)
        self.page.go("/espera_votos")

    def encerrar_espera_de_votos(self, e: ft.ControlEvent) -> None:
        self.flag_de_controle.set()
        self.process.join()
        self.mensagem = servidor.mostrar_resultados(
            self.banco_de_dados, self.udp_socket, self.mensagem
        )

        self.page.go("/resultado_host")

    def criar_nova_pauta(self, e: ft.ControlEvent) -> None:
        mensagem = "aguardando nova pauta"
        servidor.mandar_mensagem(self.banco_de_dados, self.udp_socket, mensagem)
        self.page.go("/criacao_de_pauta")

    def encerrar_sessao(self, e: ft.ControlEvent) -> None:
        self.mensagem = "sessao encerrada"
        servidor.mandar_mensagem(self.banco_de_dados, self.udp_socket, self.mensagem)
        self.page.go("/")
