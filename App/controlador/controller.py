import flet as ft
from socket import socket
from threading import Thread, Event
from servidor import servidor, cliente
from servidor.Data_Base.DB import Banco_de_Dados
import time
import threading


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
        # --- Atributos do Timer ---
        self.tempo_votacao = 0
        self.timer_control_votante = None
        self.timer_thread_votante = None
        self.stop_timer_event = threading.Event()
        self.pauta_start_timestamp = None
        # --- Fim dos Atributos do Timer ---
        self.page.go("/")

    # --- Métodos do Timer ---
    def start_voter_countdown(self):
        if (
            not self.timer_control_votante
            or self.tempo_votacao <= 0
            or self.pauta_start_timestamp is None
        ):
            return
        self.stop_voter_countdown()
        self.stop_timer_event.clear()
        self.timer_thread_votante = threading.Thread(
            target=self._voter_countdown_task, daemon=True
        )
        self.timer_thread_votante.start()

    def _voter_countdown_task(self):
        while not self.stop_timer_event.is_set():
            elapsed_time = int(time.time() - self.pauta_start_timestamp)
            current_time = max(0, self.tempo_votacao - elapsed_time)

            if self.page.route not in ["/votacao", "/confirmacao"]:
                break

            if self.timer_control_votante:
                self.timer_control_votante.value = (
                    f"Tempo restante: {current_time}s"
                    if current_time > 0
                    else "Tempo esgotado!"
                )
                try:
                    # O método page.update() é seguro para ser chamado de outras threads.
                    self.page.update()
                except Exception:
                    break

            if current_time == 0:
                # 1. Navega para a nova tela de tempo esgotado de forma segura.
                #    A correção é chamar nosso novo método '_navigate_async'.
                self.page.run_task(self._navigate_async, "/tempo_esgotado")

                # 2. A thread continua para esperar o resultado.
                self.mensagem = cliente.receber_mensagem(self.udp_socket)
                # Usa o mesmo método async para a navegação de resultado.
                self.page.run_task(self._navigate_async, "/resultado")

                # 3. Agora, espera pela próxima pauta ou encerramento.
                print("aguardando host")
                next_message = cliente.receber_mensagem(self.udp_socket)
                print(f"mensagem recebida: {next_message}")
                self.page.run_task(self._process_next_pauta_message, next_message)
                break
            time.sleep(1)

    def stop_voter_countdown(self):
        self.stop_timer_event.set()
        if self.timer_thread_votante and self.timer_thread_votante.is_alive():
            self.timer_thread_votante.join(timeout=1.0)
        self.timer_thread_votante = None

    # --- Métodos Auxiliares Async para a UI ---
    async def _navigate_async(self, route: str):
        """
        Esta é a função de "embrulho". Por ser 'async def', ela pode ser
        usada pelo 'run_task' para executar a navegação de forma segura.
        """
        self.page.go(route)

    async def _process_next_pauta_message(self, message: str):
        if message == "sessao encerrada":
            self.page.go("/")
        else:
            try:
                pauta, tempo_str = message.split("|")
                self.mensagem = pauta
                self.tempo_votacao = int(tempo_str)
                self.pauta_start_timestamp = time.time()
            except ValueError:
                self.mensagem = message
                self.tempo_votacao = 0
            self.page.go("/votacao")

    # ----------- votante -------------
    def entrar_na_votacao_como_votante(self, e: ft.ControlEvent) -> None:
        self.udp_socket = cliente.virar_votante()
        self.page.go("/espera")
        mensagem_servidor = cliente.receber_mensagem(self.udp_socket)
        try:
            pauta, tempo_str = mensagem_servidor.split("|")
            self.mensagem = pauta
            self.tempo_votacao = int(tempo_str)
            self.pauta_start_timestamp = time.time()
        except ValueError:
            self.mensagem = mensagem_servidor
            self.tempo_votacao = 0
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

        print("aguardando host")
        next_message = cliente.receber_mensagem(self.udp_socket)
        print(f"mensagem recebida: {next_message}")

        # A função de processar a próxima pauta já é async, então podemos
        # usar run_task diretamente aqui se quiséssemos rodar em thread,
        # mas como a função `confirmar_voto` bloqueia a thread principal,
        # a chamada direta é o comportamento esperado aqui.
        self._process_next_pauta_message(next_message)

    def cancelar_voto(self, e: ft.ControlEvent) -> None:
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
        campo_pauta, dropdown_tempo = e.control.data
        pauta_texto = campo_pauta.value
        tempo_selecionado = int(dropdown_tempo.value)
        self.mensagem = pauta_texto
        self.banco_de_dados.adicionar_pauta(self.mensagem)
        self.banco_de_dados.serializar_dados()
        mensagem_com_tempo = f"{self.mensagem}|{tempo_selecionado}"
        servidor.mandar_mensagem(
            self.banco_de_dados, self.udp_socket, mensagem_com_tempo
        )
        self.page.go("/sucesso_criacao_sala")
        timer_encerramento = threading.Timer(
            tempo_selecionado, self.encerrar_espera_de_votos, args=(None,)
        )
        timer_encerramento.start()
        time.sleep(5)
        self.page.go("/espera_votos")

    def encerrar_espera_de_votos(self, e: ft.ControlEvent) -> None:
        if not self.flag_de_controle.is_set():
            self.flag_de_controle.set()
            self.process.join()
            self.mensagem = servidor.mostrar_resultados(
                self.banco_de_dados, self.udp_socket, self.mensagem
            )
            self.page.go("/resultado_host")

    def criar_nova_pauta(self, e: ft.ControlEvent) -> None:
        self.page.go("/criacao_de_pauta")

    def encerrar_sessao(self, e: ft.ControlEvent) -> None:
        self.mensagem = "sessao encerrada"
        servidor.mandar_mensagem(self.banco_de_dados, self.udp_socket, self.mensagem)
        self.page.go("/")
