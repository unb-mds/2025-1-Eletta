import flet as ft
from servidor import servidor, cliente

class Controlador():
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = 'Elleta'
        self.udp_socket = None
        self.banco_de_dados = None
        self.mensagem = None
        self.process = None
        self.flag_controle = None
        self.voto_pendente = None
        self.page.go('/')

    # ----------- votante -------------
    def entrar_na_votacao_como_votante(self, e) -> None:
        self.udp_socket = cliente.virar_votante()
        self.page.go('/espera')
        pauta = cliente.receber_mensagem(self.udp_socket)
        self.mensagem = pauta
        if self.mensagem != 'votação encerrada':
            self.page.go('/votacao')

    def votar(self, e: ft.ControlEvent):
        if e.control.data == 2:
            self.voto_pendente = 'a favor'
        elif e.control.data == 1:
            self.voto_pendente = 'contra'
        elif e.control.data == 0:
            self.voto_pendente = 'nulo'
        self.page.go('/confirmacao')

    def confirmar_voto(self, e):
        try:
            cliente.votar(self.udp_socket, self.voto_pendente, self.mensagem)
            self.page.go('/espera')
            self.mensagem = cliente.receber_mensagem(self.udp_socket)
            if self.mensagem == 'votação encerrada':
                self.page.snack_bar = ft.SnackBar(ft.Text("A votação foi encerrada antes do envio do seu voto."))
                self.page.snack_bar.open = True
                self.page.update()
                self.page.go('/resultado')
                return
            self.page.go('/resultado')
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao confirmar voto: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        self.page.go('/resultado')

    def cancelar_voto(self, e):
        self.page.go('/votacao')

    def encerrar_espera_de_votos(self, e):
        self.flag_de_controle.set()
        self.process.join()
        self.mensagem = servidor.mostrar_resultados(self.banco_de_dados, self.udp_socket, self.mensagem)
        self.page.go('/resultado')
    # ----------- host -------------
    def entrar_na_votacao_como_host(self, e) -> None:
        self.udp_socket = servidor.virar_host()
        self.banco_de_dados, self.process, self.flag_de_controle = servidor.aguardar_votantes(self.udp_socket)
        self.page.go('/espera_votantes')

    def encerrar_espera_de_votantes(self, e):
        self.flag_de_controle.set()
        self.process.join()
        self.page.go('/criacao_de_pauta')

    def enviar_pauta(self, e: ft.ControlEvent):
        self.process, self.flag_de_controle = servidor.aguardar_votos(self.banco_de_dados, self.udp_socket)

        campo_texto, dropdown_tempo = e.control.data
        self.mensagem = campo_texto.value
        tempo = int(dropdown_tempo.value)  # em segundos

        self.banco_de_dados.adicionar_pauta(self.mensagem)
        self.banco_de_dados.serializar_dados()
        servidor.mandar_mensagem(self.banco_de_dados, self.udp_socket, self.mensagem)

        # Cronômetro que encerra a votação automaticamente
        def encerrar_votacao_automaticamente():
            if not self.flag_de_controle.is_set():
                self.encerrar_espera_de_votos(None)

        import threading
        threading.Timer(tempo, encerrar_votacao_automaticamente).start()

        self.page.go('/espera_votos')
