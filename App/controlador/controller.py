import flet as ft
from socket import socket, timeout
from threading import Thread, Event, Timer
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
        self.resultado_votacao: str
        self.process: Thread
        self.flag_de_controle: Event
        self.voto_pendente: str
        self.tempo_votacao = 0
        self.timer_control_votante = None
        self.timer_thread_votante = None
        self.stop_timer_event = Event()
        self.pauta_start_timestamp = None
        self.timer_encerramento = None
        self.host_ativo = False
        self.page.go("/")

    def iniciar_contagem_regressiva_votante(self):
        if (
            not self.timer_control_votante
            or self.tempo_votacao <= 0
            or self.pauta_start_timestamp is None
        ):
            return
        self.parar_contagem_regressiva_votante()
        self.stop_timer_event.clear()
        self.timer_thread_votante = Thread(
            target=self._tarefa_contagem_regressiva_votante, daemon=True
        )
        self.timer_thread_votante.start()

    def parar_contagem_regressiva_votante(self):
        self.stop_timer_event.set()
        if self.timer_thread_votante and self.timer_thread_votante.is_alive():
            self.timer_thread_votante.join(timeout=1.0)
        self.timer_thread_votante = None

    def _tarefa_contagem_regressiva_votante(self):
        self.udp_socket.settimeout(1.0)
        while not self.stop_timer_event.is_set():
            try:
                elapsed_time = int(time.time() - self.pauta_start_timestamp)
                current_time = max(0, self.tempo_votacao - elapsed_time)
                if self.page.route == "/votacao" and self.timer_control_votante:
                    self.timer_control_votante.value = (
                        f"Tempo restante: {current_time}s"
                        if current_time > 0
                        else "Tempo esgotado!"
                    )
                    self.page.update()

                try:
                    mensagem_resultado = cliente.receber_mensagem(self.udp_socket)
                    self.mensagem = mensagem_resultado

                    self.page.run_task(self._navegar_async, "/resultado")

                    self.udp_socket.settimeout(None)

                    while not self.stop_timer_event.is_set():
                        proxima_mensagem = cliente.receber_mensagem(self.udp_socket)

                        if not proxima_mensagem:
                            continue

                        if proxima_mensagem == "host_criando_nova_pauta":
                            self.page.run_task(self._navegar_async, "/aguardar_host")

                            esperar_thread = Thread(
                                target=self._tarefa_esperar_pauta, daemon=True
                            )
                            esperar_thread.start()

                        elif proxima_mensagem == "sessao encerrada":
                            self.page.run_task(self._navegar_async, "/resultado")

                            time.sleep(10)

                            self.page.run_task(self._navegar_async, "/")

                            break

                        elif "pauta:" in proxima_mensagem:
                            self.page.run_task(
                                self._processar_mensagem_pauta, proxima_mensagem
                            )
                            break

                    break
                except timeout:
                    if current_time == 0 and self.page.route in [
                        "/votacao",
                        "/confirmacao",
                    ]:
                        self.page.run_task(self._navegar_async, "/tempo_esgotado")
                    continue
            except Exception as e:
                print(f"Ocorreu um erro inesperado no loop do votante: {e}")
                time.sleep(1)
                continue

    async def _navegar_async(self, route: str):
        self.page.go(route)

    async def _processar_mensagem_pauta(self, message: str):

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

    # ----------- Votante -------------
    def _tarefa_esperar_pauta(self):

        try:
            mensagem_servidor = cliente.receber_mensagem(self.udp_socket)
            self.page.run_task(self._processar_mensagem_pauta, mensagem_servidor)
        except Exception as e:
            print(f"Erro ao aguardar pauta inicial: {e}")
            self.page.run_task(self._navegar_async, "/")

    def entrar_na_votacao_como_votante(self, e: ft.ControlEvent) -> None:
        self.page.go("/atencao_votante")

    def iniciar_escuta_votante(self, e: ft.ControlEvent) -> None:

        self.udp_socket = cliente.virar_votante()
        self.page.go("/aguardar_host")
        wait_thread = Thread(target=self._tarefa_esperar_pauta, daemon=True)
        wait_thread.start()

    def votar(self, e: ft.ControlEvent) -> None:
        if e.control.data == 2:
            self.voto_pendente = "A favor"
        elif e.control.data == 1:
            self.voto_pendente = "Contra"
        elif e.control.data == 0:
            self.voto_pendente = "Abster-se"
        self.page.go("/confirmacao")

    def confirmar_voto(self, e: ft.ControlEvent) -> None:
        cliente.votar(self.udp_socket, self.voto_pendente, self.mensagem)
        self.page.go("/sucesso_voto_computado")

    def cancelar_voto(self, e: ft.ControlEvent) -> None:
        self.page.go("/votacao")

    # ----------- Host -------------
    def entrar_na_votacao_como_host(self, e: ft.ControlEvent) -> None:
        if cliente.verificar_host_ativo():
            texto_erro = ft.Text(
                "Já existe uma sala criada para essa rede.",
                color=ft.Colors.RED_700,
                size=16,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            )
            self.page.views[0].controls.append(texto_erro)
            self.page.update()

            def remover_texto_erro():
                self.page.views[0].controls.remove(texto_erro)
                self.page.update()

            Timer(2.0, remover_texto_erro).start()
            return

        socket_host = servidor.virar_host()

        if socket_host:
            self.udp_socket = socket_host
            self.host_ativo = True
            self.banco_de_dados, self.process, self.flag_de_controle = (
                servidor.aguardar_votantes(self.udp_socket)
            )
            self.page.go("/espera_votantes")
        else:

            texto_erro = ft.Text(
                "Já existe uma sala criada para essa rede.",
                color=ft.Colors.RED_700,
                size=16,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            )

            self.page.views[0].controls.append(texto_erro)
            self.page.update()

            def remover_texto_erro():
                self.page.views[0].controls.remove(texto_erro)
                self.page.update()

            Timer(1.0, remover_texto_erro).start()

    def encerrar_espera_de_votantes(self, e: ft.ControlEvent) -> None:
        self.flag_de_controle.set()
        self.process.join()
        self.page.go("/criacao_de_pauta")

    def enviar_pauta(self, e: ft.ControlEvent) -> None:
        if self.timer_encerramento and self.timer_encerramento.is_alive():
            self.timer_encerramento.cancel()

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

        self.timer_encerramento = Timer(
            tempo_selecionado, self.encerrar_espera_de_votos, args=(None,)
        )
        self.timer_encerramento.start()

        def navegar_para_espera():
            if self.page.route == "/sucesso_criacao_sala":
                self.page.go("/espera_votos")

        Timer(2, navegar_para_espera).start()

    def encerrar_espera_de_votos(self, e: ft.ControlEvent) -> None:
        if self.timer_encerramento and self.timer_encerramento.is_alive():
            self.timer_encerramento.cancel()

        if not self.flag_de_controle.is_set():
            self.flag_de_controle.set()
            self.process.join()
            self.resultado_votacao = servidor.mostrar_resultados(
                self.banco_de_dados, self.udp_socket, self.mensagem, enviar=False
            )
            self.page.go("/resultado_host_intermediario")

    def enviar_resultado_para_votantes(self, e: ft.ControlEvent) -> None:

        if self.resultado_votacao:
            servidor.mandar_mensagem(
                self.banco_de_dados, self.udp_socket, self.resultado_votacao
            )

        dialog = ft.AlertDialog(
            title=ft.Text("Resultado enviado com sucesso!"), modal=True
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

        time.sleep(2)
        dialog.open = False
        self.page.go("/resultado_host_final")
        self.page.update()

    def criar_nova_pauta(self, e):
        self.pauta_string = None
        self.tempo_pauta = None

        servidor.mandar_mensagem(
            self.banco_de_dados, self.udp_socket, "host_criando_nova_pauta"
        )

        self.page.go("/criacao_de_pauta")

    def encerrar_sessao(self, e: ft.ControlEvent) -> None:
        self.mensagem = "sessao encerrada"
        servidor.mandar_mensagem(self.banco_de_dados, self.udp_socket, self.mensagem)
        self.host_ativo = False
        self._cleanup()
        self.page.go("/")

    def _cleanup(self):

        print("--- APP ENCERRANDO: REALIZANDO LIMPEZA ---")
        if hasattr(self, "flag_de_controle") and self.flag_de_controle:
            self.flag_de_controle.set()

        if hasattr(self, "udp_socket") and self.udp_socket:
            self.udp_socket.close()
            print("--- Porta liberada com sucesso ---")

        self.host_ativo = False

        print("--- LIMPEZA CONCLUÍDA ---")

    def verificar_status_host(self):
        self.host_ativo = cliente.verificar_host_ativo()
        return self.host_ativo

    def iniciar_verificacao_periodica_host(self, botao_votante, page):

        def verificacao_periodica():
            while True:
                time.sleep(2)
                if page.route == "/":
                    try:
                        self.verificar_status_host()
                        botao_votante.disabled = not self.host_ativo
                        page.update()
                    except Exception:
                        break
                else:
                    break

        thread_verificacao = Thread(target=verificacao_periodica, daemon=True)
        thread_verificacao.start()
