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
        # Guarda o tempo que o host definiu para a votação. Ex: 30 segundos.
        self.tempo_votacao = 0
        # Para podermos atualizar o cronômetro na tela, guardamos o componente de texto aqui.
        self.timer_control_votante = None
        # O cronômetro em si, que vai rodar "por fora" para não travar a tela.
        self.timer_thread_votante = None
        # Uma "bandeira" que usamos para avisar a thread do cronômetro que ela deve parar.
        self.stop_timer_event = threading.Event()
        # Marcamos a hora exata que a votação começou para o cronômetro funcionar direito.
        self.pauta_start_timestamp = None
        # --- Fim dos Atributos do Timer ---
        self.page.go("/")

    # --- Métodos do Timer ---
    def start_voter_countdown(self):
        """Inicia a thread de contagem regressiva para o votante."""
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
        """
        Essa função é o motor do nosso cronômetro. Ela roda por fora da interface principal
        (numa "thread") para não travar a tela enquanto atualiza o tempo a cada segundo.
        """
        while not self.stop_timer_event.is_set():
            # Calcula o tempo que falta, olhando a hora de agora e a hora que a votação começou.
            elapsed_time = int(time.time() - self.pauta_start_timestamp)
            current_time = max(0, self.tempo_votacao - elapsed_time)

            # Se o usuário mudou de tela, não tem por que o cronômetro continuar rodando.
            if self.page.route not in ["/votacao", "/confirmacao"]:
                break

            # Se temos o componente de texto guardado, atualizamos o valor dele.
            if self.timer_control_votante:
                self.timer_control_votante.value = (
                    f"Tempo restante: {current_time}s"
                    if current_time > 0
                    else "Tempo esgotado!"
                )
                try:
                    # Pedimos para a interface principal do Flet redesenhar a tela com o novo tempo.
                    self.page.update()
                except Exception:
                    # Aconteceu algum erro na atualização (ex: app fechando), então paramos.
                    break

            # Se o tempo acabou, precisamos levar o usuário para a tela de resultados.
            if current_time == 0:
                # CHEGOU A ZERO! Essa é a parte mais importante para quem não votou.
                # Avisamos a interface principal, de forma segura com o 'run_task', que o tempo
                # acabou. Ela vai se encarregar de levar o usuário para a tela de resultados.
                self.page.run_task(self.handle_timeout)
                break
            time.sleep(1)

    def stop_voter_countdown(self):
        """Usa a "bandeira" para avisar a thread do cronômetro que ela pode parar."""
        self.stop_timer_event.set()
        if self.timer_thread_votante and self.timer_thread_votante.is_alive():
            self.timer_thread_votante.join(timeout=1.0)
        self.timer_thread_votante = None

    # --- Fim dos Métodos do Timer ---

    # --- Nova Lógica de Navegação e Espera ---

    async def handle_timeout(self):
        """
        Essa função é chamada quando o cronômetro de um votante chega a zero.
        A missão dela é garantir que, mesmo sem ter votado, o usuário seja levado
        para a tela de "Aguarde o resultado" e entre na fila para receber a apuração.
        """
        # Só faz sentido agir se o usuário ainda estiver na tela de votação ou confirmação.
        if self.page.route in ["/votacao", "/confirmacao"]:
            self.page.go("/sucesso_voto_computado")
            # Aqui, o usuário que não votou entra no mesmo fluxo de quem votou:
            # ele começa a esperar pelos resultados em segundo plano.
            threading.Thread(
                target=self.wait_for_results_and_next_pauta, daemon=True
            ).start()

    def wait_for_results_and_next_pauta(self):
        """
        Aqui está a mágica da sincronização! Como receber mensagens da rede pode demorar,
        essa função roda numa thread para não congelar a tela. Ela fica pacientemente
        esperando por duas coisas: primeiro, a mensagem com os resultados; e depois, a
        mensagem com a próxima pauta (ou o aviso de que a sessão acabou).
        Tanto quem vota quanto quem deixa o tempo estourar acaba executando essa mesma função.
        """
        # 1. Primeira pausa: fica aqui esperando o servidor mandar os resultados.
        result_message = cliente.receber_mensagem(self.udp_socket)
        self.mensagem = result_message
        # Quando a mensagem chega, avisa a interface para mudar para a tela de resultados.
        self.page.run_task(self._navigate_to_route, "/resultado")

        # 2. Segunda pausa: agora, espera pela próxima instrução do host.
        print("aguardando host")
        next_message = cliente.receber_mensagem(self.udp_socket)
        print(f"mensagem recebida: {next_message}")
        # Assim que recebe, avisa a interface para processar a instrução e ir pra tela certa.
        self.page.run_task(self._process_next_pauta_message, next_message)

    async def _navigate_to_route(self, route: str):
        """Função simples só pra navegar de uma thread para outra de forma segura."""
        self.page.go(route)

    async def _process_next_pauta_message(self, message: str):
        """
        Pega a mensagem do host (após os resultados) e decide o que fazer:
        - Se for "sessao encerrada", volta pro início.
        - Se for uma nova pauta, prepara tudo para a próxima rodada de votação.
        """
        if message == "sessao encerrada":
            self.page.go("/")
        else:
            # Tenta extrair a pauta e o tempo da mensagem.
            try:
                pauta, tempo_str = message.split("|")
                self.mensagem = pauta
                self.tempo_votacao = int(tempo_str)
                self.pauta_start_timestamp = time.time()
            except ValueError:  # Se a mensagem não vier no formato "pauta|tempo".
                self.mensagem = message
                self.tempo_votacao = 0
            self.page.go("/votacao")

    # ----------- votante -------------
    def entrar_na_votacao_como_votante(self, e: ft.ControlEvent) -> None:
        self.udp_socket = cliente.virar_votante()
        self.page.go("/espera")
        mensagem_servidor = cliente.receber_mensagem(self.udp_socket)

        # A mensagem do servidor agora vem no formato "pauta|tempo".
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
        """
        Antigamente, essa função enviava o voto e ficava travada esperando a resposta.
        Agora, ela está mais esperta: ela envia o voto, leva o usuário para a tela de
        "Voto computado" e imediatamente delega a tarefa demorada de esperar o resultado
        para a nossa função 'wait_for_results_and_next_pauta', que roda por fora sem travar nada.
        """
        cliente.votar(self.udp_socket, self.voto_pendente, self.mensagem)
        cliente.votar(
            self.udp_socket, self.voto_pendente, self.mensagem
        )  # UDP não garante entrega, então enviamos 2x.
        self.page.go("/sucesso_voto_computado")
        # Inicia a thread que vai aguardar as mensagens do servidor em segundo plano.
        threading.Thread(
            target=self.wait_for_results_and_next_pauta, daemon=True
        ).start()

    def cancelar_voto(self, e: ft.ControlEvent) -> None:
        """
        Função corrigida.
        Simplesmente navega de volta para a tela de votação, sem segredo.
        """
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

        # O Host também inicia um timer. Quando o tempo acabar, ele automaticamente
        # encerra a votação e envia os resultados para todos.
        timer_encerramento = threading.Timer(
            tempo_selecionado, self.encerrar_espera_de_votos, args=(None,)
        )
        timer_encerramento.start()

        time.sleep(5)
        self.page.go("/espera_votos")

    def encerrar_espera_de_votos(self, e: ft.ControlEvent) -> None:
        # A "bandeira" garante que esta lógica de apuração só rode uma vez.
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
