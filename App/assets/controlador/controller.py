import flet as ft
import socket
from threading import Thread, Event
from servidor import servidor, cliente
from servidor.Data_Base.DB import Banco_de_Dados
import time
import threading


class Controlador:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Elleta"
        self.udp_socket: socket.socket
        self.banco_de_dados: Banco_de_Dados
        self.mensagem: str
        self.process: Thread
        self.flag_de_controle: Event
        self.voto_pendente: str
        # --- Atributos do Timer ---
        self.tempo_votacao = 0
        self.timer_control_votante = None
        self.timer_thread_votante = None
        self.stop_timer_event = threading.Event()
        self.pauta_start_timestamp = None
        # --- Fim dos Atributos do Timer ---
        self.page.go("/")

    # --- Métodos do Timer e Resultado (Traduzidos) ---
    def iniciar_contagem_regressiva_votante(self):
        if (
            not self.timer_control_votante
            or self.tempo_votacao <= 0
            or self.pauta_start_timestamp is None
        ):
            return
        self.parar_contagem_regressiva_votante()
        self.stop_timer_event.clear()
        self.timer_thread_votante = threading.Thread(
            target=self._tarefa_contagem_regressiva_votante, daemon=True
        )
        self.timer_thread_votante.start()

    def _tarefa_contagem_regressiva_votante(self):
        try:
            # Define um timeout para o socket não bloquear a execução indefinidamente.
            self.udp_socket.settimeout(1.0)

            while not self.stop_timer_event.is_set():
                elapsed_time = int(time.time() - self.pauta_start_timestamp)
                current_time = max(0, self.tempo_votacao - elapsed_time)

                if self.page.route not in [
                    "/votacao",
                    "/confirmacao",
                    "/sucesso_voto_computado",
                    "/tempo_esgotado",
                ]:
                    break

                # A atualização do timer só deve ocorrer na tela de votação.
                if self.page.route == "/votacao" and self.timer_control_votante:
                    self.timer_control_votante.value = (
                        f"Tempo restante: {current_time}s"
                        if current_time > 0
                        else "Tempo esgotado!"
                    )
                    try:
                        self.page.update()
                    except Exception:
                        # Se a UI falhar, NÃO interrompa a thread. Apenas ignore o erro.
                        # Interromper a thread era a causa principal do congelamento, pois
                        # impedia o recebimento da mensagem com o resultado da votação.
                        pass

                try:
                    # Tenta receber uma mensagem (o resultado) do servidor.
                    mensagem_resultado = cliente.receber_mensagem(self.udp_socket)

                    # Se uma mensagem for recebida, é o resultado.
                    self.mensagem = mensagem_resultado
                    self.page.run_task(self._navegar_async, "/resultado")

                    # Aguarda a próxima pauta ou o encerramento da sessão.
                    print("aguardando host pela proxima pauta...")
                    self.udp_socket.settimeout(
                        None
                    )  # Espera indefinidamente pela próxima mensagem.
                    next_message = cliente.receber_mensagem(self.udp_socket)
                    print(f"mensagem recebida: {next_message}")
                    self.page.run_task(self._processar_mensagem_pauta, next_message)
                    break  # Encerra o loop.

                except socket.timeout:
                    # Nenhuma mensagem recebida, o que é normal. Continua o loop.
                    if current_time == 0:
                        if self.page.route == "/votacao":
                            self.page.run_task(self._navegar_async, "/tempo_esgotado")
                    continue

                except Exception as e:
                    print(f"Ocorreu um erro na tarefa do votante: {e}")
                    # Também não interromper aqui para garantir a robustez.
                    pass
        except Exception as e:
            print(f"Erro fatal na thread do votante: {e}")
            return

    def parar_contagem_regressiva_votante(self):
        self.stop_timer_event.set()
        if self.timer_thread_votante and self.timer_thread_votante.is_alive():
            self.timer_thread_votante.join(timeout=1.0)
        self.timer_thread_votante = None

    # --- Métodos Auxiliares Async para a UI ---
    async def _navegar_async(self, route: str):
        """
        Esta é a função de "embrulho". Por ser 'async def', ela pode ser
        usada pelo 'run_task' para executar a navegação de forma segura.
        """
        self.page.go(route)

    async def _processar_mensagem_pauta(self, message: str):
        """Processa uma mensagem de pauta (inicial ou subsequente) e navega para a votação."""
        if message == "sessao encerrada" or message == "votação encerrada":
            self.page.go("/")
            return

        try:
            pauta, tempo_str = message.split("|")
            self.mensagem = pauta
            self.tempo_votacao = int(tempo_str)
            self.pauta_start_timestamp = time.time()
        except ValueError:
            self.mensagem = message
            self.tempo_votacao = 0
            self.pauta_start_timestamp = time.time()

        if self.mensagem:
            self.page.go("/votacao")

    # ----------- votante -------------
    def _tarefa_esperar_pauta(self):
        """Roda em uma thread, esperando a pauta inicial sem bloquear a UI."""
        try:
            mensagem_servidor = cliente.receber_mensagem(self.udp_socket)
            self.page.run_task(self._processar_mensagem_pauta, mensagem_servidor)
        except Exception as e:
            print(f"Erro ao aguardar pauta inicial: {e}")
            self.page.run_task(self._navegar_async, "/")

    def entrar_na_votacao_como_votante(self, e: ft.ControlEvent) -> None:
        """Navega para a tela de atenção."""
        self.page.go("/atencao_votante")

    def iniciar_escuta_votante(self, e: ft.ControlEvent) -> None:
        """Inicia o fluxo do votante de forma não-bloqueante após a tela de atenção."""
        self.udp_socket = cliente.virar_votante()
        self.page.go("/aguardar_host")
        # Inicia uma thread para esperar a pauta sem congelar a UI.
        wait_thread = threading.Thread(target=self._tarefa_esperar_pauta, daemon=True)
        wait_thread.start()

    def votar(self, e: ft.ControlEvent) -> None:
        if e.control.data == 2:
            self.voto_pendente = "a favor"
        elif e.control.data == 1:
            self.voto_pendente = "contra"
        elif e.control.data == 0:
            self.voto_pendente = "nulo"
        self.page.go("/confirmacao")

    def confirmar_voto(self, e: ft.ControlEvent) -> None:
        # Envia o voto para o servidor.
        cliente.votar(self.udp_socket, self.voto_pendente, self.mensagem)
        # Redireciona para a tela de sucesso. A tarefa de fundo (_tarefa_contagem_regressiva_votante)
        # agora é responsável por aguardar o resultado e fazer a navegação.
        self.page.go("/sucesso_voto_computado")

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
