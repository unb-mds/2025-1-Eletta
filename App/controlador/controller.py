import flet as ft
from socket import socket, timeout
from threading import Thread, Event, Timer
from servidor import servidor, cliente
from servidor.Data_Base.DB import Banco_de_Dados
import time


class Controlador:
    def __init__(self, page: ft.Page):
        # Inicializa o Controlador principal da aplicação.#
        self.page = page
        self.page.title = "Elleta"
        self.udp_socket: socket
        self.banco_de_dados: Banco_de_Dados
        self.mensagem: str
        self.resultado_votacao: str
        self.process: Thread
        self.flag_de_controle: Event
        self.voto_pendente: str
        # --- Atributos do Timer ---
        self.tempo_votacao = 0
        self.timer_control_votante = None
        self.timer_thread_votante = None
        self.stop_timer_event = Event()
        self.pauta_start_timestamp = None
        # --- Atributo para guardar o timer de encerramento ---
        self.timer_encerramento = None
        # --- Atributo para verificar se há host ativo ---
        self.host_ativo = False
        # --- Fim dos Atributos do Timer ---
        self.page.go("/")

    # --- Métodos do Timer e Resultado ---
    def iniciar_contagem_regressiva_votante(self):
        # Inicia a thread para a contagem regressiva do tempo de votação na tela do votante.
        if (
            not self.timer_control_votante
            or self.tempo_votacao <= 0
            or self.pauta_start_timestamp is None
        ):
            return
        # Garante que qualquer thread antiga seja parada antes de iniciar uma nova.
        self.parar_contagem_regressiva_votante()
        self.stop_timer_event.clear()
        self.timer_thread_votante = Thread(
            target=self._tarefa_contagem_regressiva_votante, daemon=True
        )
        self.timer_thread_votante.start()

    def parar_contagem_regressiva_votante(self):
        # Sinaliza e aguarda a thread do timer atual terminar.#
        self.stop_timer_event.set()
        if self.timer_thread_votante and self.timer_thread_votante.is_alive():
            self.timer_thread_votante.join(timeout=1.0)  # Espera no máximo 1s
        self.timer_thread_votante = None

    def _tarefa_contagem_regressiva_votante(self):
        # Loop principal do votante que executa em uma thread.
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

                    # Navega para a tela de resultados.
                    self.page.run_task(self._navegar_async, "/resultado")

                    # Define um timeout infinito para aguardar a próxima instrução do host.
                    self.udp_socket.settimeout(None)

                    # Loop para aguardar a próxima ação do host (nova pauta ou fim da sessão)
                    while not self.stop_timer_event.is_set():
                        proxima_mensagem = cliente.receber_mensagem(self.udp_socket)

                        if not proxima_mensagem:
                            continue

                        if proxima_mensagem == "host_criando_nova_pauta":
                            # O host iniciou a criação de uma nova pauta. Mostra a tela de aguardo.
                            self.page.run_task(self._navegar_async, "/aguardar_host")

                            # Reinicia a escuta da nova pauta
                            esperar_thread = Thread(
                                target=self._tarefa_esperar_pauta, daemon=True
                            )
                            esperar_thread.start()

                        elif proxima_mensagem == "sessao encerrada":
                            # Mostra a tela de resultado
                            self.page.run_task(self._navegar_async, "/resultado")

                            # Espera 10 segundos para o votante ver o resultado
                            time.sleep(10)

                            # Navega para a tela inicial
                            self.page.run_task(self._navegar_async, "/")

                            break

                        elif "pauta:" in proxima_mensagem:
                            # O host enviou uma nova pauta
                            self.page.run_task(
                                self._processar_mensagem_pauta, proxima_mensagem
                            )
                            break

                    break  # Sai do loop de contagem regressiva, a tarefa desta thread está completa.

                except timeout:
                    # Lógica de timeout existente (quando o tempo de votação acaba).
                    if current_time == 0 and self.page.route in [
                        "/votacao",
                        "/confirmacao",
                    ]:
                        self.page.run_task(self._navegar_async, "/tempo_esgotado")
                    continue
            except Exception as e:
                # Se um erro inesperado ocorrer, registra e continua tentando.
                print(f"Ocorreu um erro inesperado no loop do votante: {e}")
                time.sleep(1)
                continue

    # --- Métodos Auxiliares Async para a UI ---
    async def _navegar_async(self, route: str):
        # Navega para uma rota de forma assíncrona, segura para threads.#
        self.page.go(route)

    async def _processar_mensagem_pauta(self, message: str):
        # Processa uma mensagem de pauta (inicial ou subsequente) e navega para a votação. A mensagem deve ter o formato "Texto da Pauta|tempo_em_segundos".

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
        # Roda em uma thread, esperando a pauta inicial sem bloquear a UI.
        try:
            mensagem_servidor = cliente.receber_mensagem(self.udp_socket)
            # Usa run_task para interagir com a UI a partir de uma thread
            self.page.run_task(self._processar_mensagem_pauta, mensagem_servidor)
        except Exception as e:
            print(f"Erro ao aguardar pauta inicial: {e}")
            self.page.run_task(self._navegar_async, "/")

    def entrar_na_votacao_como_votante(self, e: ft.ControlEvent) -> None:
        # Navega para a tela de atenção inicial do votante.
        self.page.go("/atencao_votante")

    def iniciar_escuta_votante(self, e: ft.ControlEvent) -> None:
        # Inicia o fluxo do votante de forma não-bloqueante após a tela de atenção.

        self.udp_socket = cliente.virar_votante()
        self.page.go("/aguardar_host")
        # Inicia uma thread para esperar a pauta sem congelar a UI.
        wait_thread = Thread(target=self._tarefa_esperar_pauta, daemon=True)
        wait_thread.start()

    def votar(self, e: ft.ControlEvent) -> None:
        # Armazena o voto pendente e navega para a tela de confirmação.#
        if e.control.data == 2:
            self.voto_pendente = "A favor"
        elif e.control.data == 1:
            self.voto_pendente = "Contra"
        elif e.control.data == 0:
            self.voto_pendente = "Abster-se"
        self.page.go("/confirmacao")

    def confirmar_voto(self, e: ft.ControlEvent) -> None:
        # Envia o voto pendente para o servidor e vai para a tela de sucesso.
        cliente.votar(self.udp_socket, self.voto_pendente, self.mensagem)
        self.page.go("/sucesso_voto_computado")

    def cancelar_voto(self, e: ft.ControlEvent) -> None:
        # Cancela a seleção do voto e volta para a tela de votação.
        self.page.go("/votacao")

    # ----------- Host -------------
    def entrar_na_votacao_como_host(self, e: ft.ControlEvent) -> None:
        """
        Tenta iniciar o modo host. Se já existir um, exibe uma mensagem
        temporária na tela que desaparece após 1 segundo.
        """
        socket_host = servidor.virar_host()

        if socket_host:
            # SUCESSO: O fluxo continua como antes.
            self.udp_socket = socket_host
            self.host_ativo = True  # Define que este cliente agora é o host
            self.banco_de_dados, self.process, self.flag_de_controle = (
                servidor.aguardar_votantes(self.udp_socket)
            )
            self.page.go("/espera_votantes")
        else:
            # FALHA: Um host já existe. Exibe uma mensagem de texto que some em 2s.

            # 1. Cria o controle de texto do erro.
            texto_erro = ft.Text(
                "Já existe uma sala criada para essa rede.",
                color=ft.Colors.RED_700,
                size=16,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            )

            # 2. Adiciona o texto à tela e atualiza para que ele apareça.
            self.page.views[0].controls.append(texto_erro)
            self.page.update()

            # 3. Define uma função para remover o texto e atualizar a tela novamente.
            def remover_texto_erro():
                self.page.views[0].controls.remove(texto_erro)
                self.page.update()

            # 4. Inicia um timer que chamará a função de remoção após 2 segundos.
            Timer(1.0, remover_texto_erro).start()

    def encerrar_espera_de_votantes(self, e: ft.ControlEvent) -> None:
        # Encerra a fase de aguardar novos votantes e navega para a criação de pauta.
        self.flag_de_controle.set()
        self.process.join()
        self.page.go("/criacao_de_pauta")

    def enviar_pauta(self, e: ft.ControlEvent) -> None:
        # Envia a pauta e o tempo para os votantes e inicia o timer de votação.#

        # --- Cancela qualquer timer anterior que ainda possa estar ativo ---
        if self.timer_encerramento and self.timer_encerramento.is_alive():
            self.timer_encerramento.cancel()
        # --- ---

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

        # --- Armazena o novo timer na instância do controlador ---
        self.timer_encerramento = Timer(
            tempo_selecionado, self.encerrar_espera_de_votos, args=(None,)
        )
        self.timer_encerramento.start()
        # --- FIM DA CORREÇÃO ---

        def navegar_para_espera():
            if self.page.route == "/sucesso_criacao_sala":
                self.page.go("/espera_votos")

        Timer(2, navegar_para_espera).start()

    def encerrar_espera_de_votos(self, e: ft.ControlEvent) -> None:
        # Encerra a votação, calcula os resultados e navega para a tela de resultados do host, SEM enviar aos votantes.
        if self.timer_encerramento and self.timer_encerramento.is_alive():
            self.timer_encerramento.cancel()

        if not self.flag_de_controle.is_set():
            self.flag_de_controle.set()
            self.process.join()
            # Apenas calcula o resultado e armazena no atributo da classe
            self.resultado_votacao = servidor.mostrar_resultados(
                self.banco_de_dados, self.udp_socket, self.mensagem, enviar=False
            )
            self.page.go("/resultado_host_intermediario")

    def enviar_resultado_para_votantes(self, e: ft.ControlEvent) -> None:
        """
        Envia o resultado armazenado para todos os votantes e, em seguida,
        navega o host para a tela final de resultados.
        """
        if self.resultado_votacao:
            servidor.mandar_mensagem(
                self.banco_de_dados, self.udp_socket, self.resultado_votacao
            )

        # Simula o pop-up de sucesso e depois vai para a tela final
        dialog = ft.AlertDialog(
            title=ft.Text("Resultado enviado com sucesso!"), modal=True
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

        # Após um tempo, fecha o diálogo e vai para a tela final de resultado do host
        time.sleep(2)
        dialog.open = False
        self.page.go("/resultado_host_final")
        self.page.update()

    def criar_nova_pauta(self, e):
        """Chamado quando o host clica em 'Criar Nova Pauta'."""
        # Limpa o estado da pauta anterior.
        self.pauta_string = None
        self.tempo_pauta = None

        # Adicionado o argumento self.banco_de_dados que estava faltando.
        servidor.mandar_mensagem(
            self.banco_de_dados, self.udp_socket, "host_criando_nova_pauta"
        )

        # Navega o host para a tela de criação de pauta.
        self.page.go("/criacao_de_pauta")

    def encerrar_sessao(self, e: ft.ControlEvent) -> None:
        # Envia uma mensagem de encerramento para todos os votantes e volta para a tela inicial.
        self.mensagem = "sessao encerrada"
        servidor.mandar_mensagem(self.banco_de_dados, self.udp_socket, self.mensagem)
        self.host_ativo = False  # Define que não há mais host ativo
        self._cleanup()
        self.page.go("/")

    def _cleanup(self):

        print("--- APP ENCERRANDO: REALIZANDO LIMPEZA ---")
        if hasattr(self, "flag_de_controle") and self.flag_de_controle:
            self.flag_de_controle.set()

        # Fecha o socket de rede se ele existir
        if hasattr(self, "udp_socket") and self.udp_socket:
            self.udp_socket.close()
            print("--- Porta liberada com sucesso ---")

        # Define que não há mais host ativo
        self.host_ativo = False

        print("--- LIMPEZA CONCLUÍDA ---")

    # --- Métodos do Timer e Resultado ---
    def verificar_status_host(self):
        """Verifica se há um host ativo na rede e atualiza o status."""
        self.host_ativo = cliente.verificar_host_ativo()
        return self.host_ativo

    def iniciar_verificacao_periodica_host(self, botao_votante, page):
        """Inicia a verificação periódica do status do host e atualiza o botão."""

        def verificacao_periodica():
            while True:
                time.sleep(2)  # Verifica a cada 2 segundos
                if page.route == "/":  # Só verifica se estiver na página inicial
                    try:
                        self.verificar_status_host()
                        botao_votante.disabled = not self.host_ativo
                        page.update()
                    except Exception:
                        break  # Para a thread se a página não existir mais
                else:
                    break  # Para a thread se sair da página inicial

        # Inicia a verificação em uma thread separada
        thread_verificacao = Thread(target=verificacao_periodica, daemon=True)
        thread_verificacao.start()
