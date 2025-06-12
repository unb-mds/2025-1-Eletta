import flet as ft
import socket
from threading import Thread, Event
from servidor import servidor, cliente
from servidor.Data_Base.DB import Banco_de_Dados
import time
import threading


class Controlador:
    def __init__(self, page: ft.Page):
        """Inicializa o Controlador principal da aplicação."""
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

    # --- Métodos do Timer e Resultado ---
    def iniciar_contagem_regressiva_votante(self):
        """
        Inicia a thread para a contagem regressiva do tempo de votação na tela do votante.
        """
        if (
            not self.timer_control_votante
            or self.tempo_votacao <= 0
            or self.pauta_start_timestamp is None
        ):
            return
        # Garante que qualquer thread antiga seja parada antes de iniciar uma nova.
        self.parar_contagem_regressiva_votante()
        self.stop_timer_event.clear()
        self.timer_thread_votante = threading.Thread(
            target=self._tarefa_contagem_regressiva_votante, daemon=True
        )
        self.timer_thread_votante.start()

    def parar_contagem_regressiva_votante(self):
        """Sinaliza e aguarda a thread do timer atual terminar."""
        self.stop_timer_event.set()
        if self.timer_thread_votante and self.timer_thread_votante.is_alive():
            self.timer_thread_votante.join(timeout=1.0)  # Espera no máximo 1s
        self.timer_thread_votante = None

    def _tarefa_contagem_regressiva_votante(self):
        """
        [VERSÃO CORRIGIDA E ROBUSTA]
        Loop principal do votante que executa em uma thread.
        Esta versão é mais resistente a falhas de rede e não termina prematuramente.
        """
        self.udp_socket.settimeout(1.0)
        while not self.stop_timer_event.is_set():
            try:
                # ----- Lógica do Cronômetro -----
                elapsed_time = int(time.time() - self.pauta_start_timestamp)
                current_time = max(0, self.tempo_votacao - elapsed_time)
                if self.page.route == "/votacao" and self.timer_control_votante:
                    self.timer_control_votante.value = (
                        f"Tempo restante: {current_time}s"
                        if current_time > 0
                        else "Tempo esgotado!"
                    )
                    self.page.update()

                # ----- Lógica de Rede (Recebimento de Mensagem) -----
                try:
                    # Tenta receber uma mensagem (o resultado) do servidor.
                    mensagem_resultado = cliente.receber_mensagem(self.udp_socket)
                    self.mensagem = mensagem_resultado
                    self.page.run_task(self._navegar_async, "/resultado")

                    # Agora, aguarda a próxima instrução do host.
                    self.udp_socket.settimeout(None)
                    next_message = cliente.receber_mensagem(self.udp_socket)
                    self.page.run_task(self._processar_mensagem_pauta, next_message)
                    break  # Sai do loop while após processar o resultado.

                except socket.timeout:
                    # Isso é normal. Nenhuma mensagem foi recebida no último segundo.
                    if current_time == 0 and self.page.route == "/votacao":
                        self.page.run_task(self._navegar_async, "/tempo_esgotado")
                    continue
            except Exception as e:
                # Se um erro inesperado ocorrer, registra e continua tentando.
                print(f"Ocorreu um erro inesperado no loop do votante: {e}")
                time.sleep(1)
                continue

    # --- Métodos Auxiliares Async para a UI ---
    async def _navegar_async(self, route: str):
        """Navega para uma rota de forma assíncrona, segura para threads."""
        self.page.go(route)

    async def _processar_mensagem_pauta(self, message: str):
        """
        Processa uma mensagem de pauta (inicial ou subsequente) e navega para a votação.
        A mensagem deve ter o formato "Texto da Pauta|tempo_em_segundos".
        """
        if message == "sessao encerrada" or message == "votação encerrada":
            self.page.go("/")
            return
        try:
            pauta, tempo_str = message.split("|")
            self.mensagem = pauta
            self.tempo_votacao = int(tempo_str)
            self.pauta_start_timestamp = time.time()
        except ValueError:
            # Caso a mensagem não venha no formato esperado
            self.mensagem = message
            self.tempo_votacao = 0  # Define um tempo padrão ou lida com o erro
            self.pauta_start_timestamp = time.time()

        if self.mensagem:
            self.page.go("/votacao")

    # ----------- Votante -------------
    def _tarefa_esperar_pauta(self):
        """
        Roda em uma thread, esperando a pauta inicial sem bloquear a UI.
        """
        try:
            mensagem_servidor = cliente.receber_mensagem(self.udp_socket)
            # Usa run_task para interagir com a UI a partir de uma thread
            self.page.run_task(self._processar_mensagem_pauta, mensagem_servidor)
        except Exception as e:
            print(f"Erro ao aguardar pauta inicial: {e}")
            self.page.run_task(self._navegar_async, "/")

    def entrar_na_votacao_como_votante(self, e: ft.ControlEvent) -> None:
        """Navega para a tela de atenção inicial do votante."""
        self.page.go("/atencao_votante")

    def iniciar_escuta_votante(self, e: ft.ControlEvent) -> None:
        """
        Inicia o fluxo do votante de forma não-bloqueante após a tela de atenção.
        """
        self.udp_socket = cliente.virar_votante()
        self.page.go("/aguardar_host")
        # Inicia uma thread para esperar a pauta sem congelar a UI.
        wait_thread = threading.Thread(target=self._tarefa_esperar_pauta, daemon=True)
        wait_thread.start()

    def votar(self, e: ft.ControlEvent) -> None:
        """Armazena o voto pendente e navega para a tela de confirmação."""
        if e.control.data == 2:
            self.voto_pendente = "a favor"
        elif e.control.data == 1:
            self.voto_pendente = "contra"
        elif e.control.data == 0:
            self.voto_pendente = "nulo"
        self.page.go("/confirmacao")

    def confirmar_voto(self, e: ft.ControlEvent) -> None:
        """Envia o voto pendente para o servidor e vai para a tela de sucesso."""
        cliente.votar(self.udp_socket, self.voto_pendente, self.mensagem)
        self.page.go("/sucesso_voto_computado")

    def cancelar_voto(self, e: ft.ControlEvent) -> None:
        """Cancela a seleção do voto e volta para a tela de votação."""
        self.page.go("/votacao")

    # ----------- Host -------------
    def entrar_na_votacao_como_host(self, e: ft.ControlEvent) -> None:
        """Inicia o modo host, cria o socket e vai para a tela de espera por votantes."""
        self.udp_socket = servidor.virar_host()
        self.banco_de_dados, self.process, self.flag_de_controle = (
            servidor.aguardar_votantes(self.udp_socket)
        )
        self.page.go("/espera_votantes")

    def encerrar_espera_de_votantes(self, e: ft.ControlEvent) -> None:
        """Encerra a fase de aguardar novos votantes e navega para a criação de pauta."""
        self.flag_de_controle.set()
        self.process.join()
        self.page.go("/criacao_de_pauta")

    def enviar_pauta(self, e: ft.ControlEvent) -> None:
        """Envia a pauta e o tempo para os votantes e inicia o timer de votação."""
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

        # O time.sleep(5) que estava aqui foi REMOVIDO pois congelava a interface do host.
        # A navegação para a tela de espera agora é feita de forma não-bloqueante.
        def navegar_para_espera():
            if self.page.route == "/sucesso_criacao_sala":
                self.page.go("/espera_votos")

        threading.Timer(2, navegar_para_espera).start()

    def encerrar_espera_de_votos(self, e: ft.ControlEvent) -> None:
        """Encerra a votação, calcula os resultados e navega para a tela de resultados do host."""
        if not self.flag_de_controle.is_set():
            self.flag_de_controle.set()
            self.process.join()
            self.mensagem = servidor.mostrar_resultados(
                self.banco_de_dados, self.udp_socket, self.mensagem
            )
            self.page.go("/resultado_host")

    def criar_nova_pauta(self, e: ft.ControlEvent) -> None:
        """Navega de volta para a tela de criação de pauta para uma nova rodada."""
        self.page.go("/criacao_de_pauta")

    def encerrar_sessao(self, e: ft.ControlEvent) -> None:
        """Envia uma mensagem de encerramento para todos os votantes e volta para a tela inicial."""
        self.mensagem = "sessao encerrada"
        servidor.mandar_mensagem(self.banco_de_dados, self.udp_socket, self.mensagem)
        self.page.go("/")
