import threading
import time
import flet as ft
from servidor import cliente, servidor
from servidor.Data_Base.DB import Banco_de_Dados
from socket import socket


class Controlador:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Elleta"
        self.udp_socket: socket = None
        self.banco_de_dados: Banco_de_Dados = None
        self.mensagem: str = ""
        self.process: threading.Thread = None
        self.flag_de_controle: threading.Event = None
        self.voto_pendente: str = ""

        # Atributos do Timer
        self.tempo_votacao = 0
        self.timer_control_votante = None
        self.timer_thread_votante = None
        self.stop_timer_event = threading.Event()
        self.pauta_start_timestamp = None
        self.current_pauta_text = None

        # Atributos do Ouvinte Contínuo do Votante
        self.voter_listener_thread = None
        self.is_voter = False

        self.page.go("/")

    # --- Nova Arquitetura do Votante ---

    def start_voter_listener(self):
        """Inicia o loop de escuta contínuo do votante em segundo plano."""
        if (
            self.voter_listener_thread is None
            or not self.voter_listener_thread.is_alive()
        ):
            self.is_voter = True
            self.voter_listener_thread = threading.Thread(
                target=self._voter_message_processor, daemon=True
            )
            self.voter_listener_thread.start()

    def stop_voter_listener(self):
        """Para o loop de escuta do votante."""
        self.is_voter = False

    def _voter_message_processor(self):
        """
        Este é o coração do votante. Ele roda em uma thread dedicada e fica
        escutando continuamente as mensagens do servidor.
        """
        while self.is_voter:
            try:
                # Bloqueia a execução desta thread até uma mensagem chegar
                mensagem_recebida = cliente.receber_mensagem(self.udp_socket)

                # Despacha a mensagem para ser processada na thread da UI, que é seguro
                self.page.run_task(self.handle_server_message, mensagem_recebida)
            except Exception as e:
                print(f"Erro no loop de escuta do votante: {e}")
                self.stop_voter_listener()
                break

    async def handle_server_message(self, message: str):
        """
        Processa TODAS as mensagens do servidor na thread principal da UI.
        É o cérebro que decide para qual tela navegar.
        """
        self.stop_voter_countdown()

        if "sessao encerrada" in message:
            self.mensagem = "A sessão foi encerrada pelo Host."
            self.stop_voter_listener()
            self.page.go("/")
            return

        if "Resultado da votação" in message:
            self.mensagem = message
            self.page.go("/resultado")
            return

        try:
            partes = message.split("|", 1)
            if len(partes) == 2:
                nova_pauta_texto, novo_tempo_votacao_str = partes
                self.current_pauta_text = nova_pauta_texto
                self.pauta_start_timestamp = time.time()
                self.mensagem = nova_pauta_texto
                self.tempo_votacao = int(novo_tempo_votacao_str)
                self.page.go("/votacao")
        except Exception as e:
            print(f"Erro ao processar mensagem do servidor: {e}")

    # --- Funções do Votante (Modificadas) ---

    def entrar_na_votacao_como_votante(self, e: ft.ControlEvent) -> None:
        if self.udp_socket is None:
            self.udp_socket = cliente.virar_votante()
        self.page.go("/espera")
        # Inicia o ouvinte contínuo
        self.start_voter_listener()

    def confirmar_voto(self, e: ft.ControlEvent):
        """Agora esta função apenas envia o voto. O ouvinte cuidará do resto."""
        if self.voto_pendente and self.mensagem:
            cliente.votar(self.udp_socket, self.voto_pendente, self.mensagem)
            # Vai para uma tela de sucesso temporária
            self.page.go("/sucesso_voto_computado")
            # O ouvinte em background receberá o resultado e navegará para a tela correta.

    # --- Funções do Votante (sem grandes mudanças) ---

    def votar(self, e: ft.ControlEvent):
        voto_map = {2: "a favor", 1: "contra", 0: "nulo"}
        self.voto_pendente = voto_map.get(e.control.data)
        self.page.go("/confirmacao")

    def cancelar_voto(self, e: ft.ControlEvent):
        self.page.go("/votacao")

    def start_voter_countdown(self):
        if (
            not self.timer_control_votante
            or self.tempo_votacao <= 0
            or self.pauta_start_timestamp is None
        ):
            if self.timer_control_votante:
                self.timer_control_votante.value = "Aguardando início do tempo..."
            try:
                self.page.update()
            except Exception:
                pass
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
                    self.page.update()
                except Exception:
                    break
            if current_time == 0:
                break
            time.sleep(1)

    def stop_voter_countdown(self):
        self.stop_timer_event.set()
        if self.timer_thread_votante and self.timer_thread_votante.is_alive():
            self.timer_thread_votante.join(timeout=1.0)
        self.timer_thread_votante = None

    # ----------- Funções do Host (inalteradas) -------------

    def entrar_na_votacao_como_host(self, e: ft.ControlEvent) -> None:
        self.stop_voter_listener()  # Garante que o modo votante está desativado
        self.udp_socket = servidor.virar_host()
        self.banco_de_dados, self.process, self.flag_de_controle = (
            servidor.aguardar_votantes(self.udp_socket)
        )
        self.page.go("/espera_votantes")

    def encerrar_espera_de_votantes(self, e: ft.ControlEvent) -> None:
        self.flag_de_controle.set()
        self.process.join()
        self.page.go("/criacao_de_pauta")

    def enviar_pauta(self, e: ft.ControlEvent):
        self.process, self.flag_de_controle = servidor.aguardar_votos(
            self.banco_de_dados, self.udp_socket
        )
        campo_texto, dropdown_tempo = e.control.data
        pauta_texto = campo_texto.value or "Pauta não definida"
        self.mensagem = pauta_texto
        tempo = int(dropdown_tempo.value)
        self.banco_de_dados.adicionar_pauta(self.mensagem)
        self.banco_de_dados.serializar_dados()
        mensagem_com_tempo = f"{self.mensagem}|{tempo}"
        servidor.mandar_mensagem(
            self.banco_de_dados, self.udp_socket, mensagem_com_tempo
        )
        self.page.go("/sucesso_criacao_sala")
        threading.Timer(
            tempo, lambda: self.page.run_task(self.encerrar_espera_de_votos_async)
        ).start()
        time.sleep(3)
        self.page.go("/espera_votos")

    async def encerrar_espera_de_votos_async(self):
        if not self.flag_de_controle.is_set():
            self.flag_de_controle.set()
            self.process.join()
            self.mensagem = servidor.mostrar_resultados(
                self.banco_de_dados, self.udp_socket, self.mensagem
            )
            self.page.go("/resultado_host")

    def encerrar_espera_de_votos(self, e: ft.ControlEvent):
        self.page.run_task(self.encerrar_espera_de_votos_async)

    def criar_nova_pauta(self, e: ft.ControlEvent) -> None:
        self.page.go("/criacao_de_pauta")

    def encerrar_sessao(self, e: ft.ControlEvent) -> None:
        self.mensagem = "sessao encerrada"
        servidor.mandar_mensagem(self.banco_de_dados, self.udp_socket, self.mensagem)
        self.page.go("/")
