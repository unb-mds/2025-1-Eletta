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
        self.socket_udp: socket
        self.banco_de_dados: Banco_de_Dados
        self.mensagem: str
        self.resultado_votacao: str
        self.processo_de_escuta: Thread
        self.flag_de_controle: Event
        self.voto_pendente: str
        self.tempo_votacao = 0
        self.controle_do_timer_votante = None
        self.thread_do_timer_votante = None
        self.parar_timer_evento = Event()
        self.timestamp_inicio_pauta = None
        self.timer_encerramento = None
        self.host_ativo = False
        self.page.go("/")

    def iniciar_contagem_regressiva_votante(self):
        if (
            not self.controle_do_timer_votante
            or self.tempo_votacao <= 0
            or self.timestamp_inicio_pauta is None
        ):
            return
        self.parar_contagem_regressiva_votante()
        self.parar_timer_evento.clear()
        self.thread_do_timer_votante = Thread(
            target=self._tarefa_contagem_regressiva_votante, daemon=True
        )
        self.thread_do_timer_votante.start()

    def parar_contagem_regressiva_votante(self):
        self.parar_timer_evento.set()
        if self.thread_do_timer_votante and self.thread_do_timer_votante.is_alive():
            self.thread_do_timer_votante.join(timeout=1.0)
        self.thread_do_timer_votante = None

    def _tarefa_contagem_regressiva_votante(self):
        self.socket_udp.settimeout(1.0)
        while not self.parar_timer_evento.is_set():
            try:
                tempo_decorrido = int(time.time() - self.timestamp_inicio_pauta)
                tempo_atual = max(0, self.tempo_votacao - tempo_decorrido)
                if self.page.route == "/votacao" and self.controle_do_timer_votante:
                    self.controle_do_timer_votante.value = (
                        f"Tempo restante: {tempo_atual}s"
                        if tempo_atual > 0
                        else "Tempo esgotado!"
                    )
                    self.page.update()

                try:
                    mensagem_resultado = cliente.receber_mensagem(self.socket_udp)
                    self.mensagem = mensagem_resultado

                    self.page.run_task(self._navegar_assincrono, "/resultado")

                    self.socket_udp.settimeout(None)

                    while not self.parar_timer_evento.is_set():
                        proxima_mensagem = cliente.receber_mensagem(self.socket_udp)

                        if not proxima_mensagem:
                            continue

                        if proxima_mensagem == "host_criando_nova_pauta":
                            self.page.run_task(self._navegar_assincrono, "/aguardar_host")

                            thread_espera = Thread(
                                target=self._tarefa_esperar_pauta, daemon=True
                            )
                            thread_espera.start()

                        elif proxima_mensagem == "sessao encerrada":
                            self.page.run_task(self._navegar_assincrono, "/resultado")

                            time.sleep(10)

                            self.page.run_task(self._navegar_assincrono, "/")

                            break

                        elif "pauta:" in proxima_mensagem:
                            self.page.run_task(
                                self._processar_mensagem_pauta, proxima_mensagem
                            )
                            break

                    break
                except timeout:
                    if tempo_atual == 0 and self.page.route in [
                        "/votacao",
                        "/confirmacao",
                    ]:
                        self.page.run_task(self._navegar_assincrono, "/tempo_esgotado")
                    continue
            except Exception as e:
                print(f"Ocorreu um erro inesperado no laço do votante: {e}")
                time.sleep(1)
                continue

    async def _navegar_assincrono(self, rota: str):
        self.page.go(rota)

    async def _processar_mensagem_pauta(self, mensagem: str):

        if mensagem == "sessao encerrada" or mensagem == "votação encerrada":
            self.page.go("/")
            return
        try:
            pauta, tempo_str = mensagem.split("|")
            self.mensagem = pauta
            self.tempo_votacao = int(tempo_str)
            self.timestamp_inicio_pauta = time.time()
        except ValueError:
            self.mensagem = mensagem
            self.tempo_votacao = 0
            self.timestamp_inicio_pauta = time.time()

        if self.mensagem:
            self.page.go("/votacao")

    # ----------- Votante -------------
    def _tarefa_esperar_pauta(self):

        try:
            mensagem_servidor = cliente.receber_mensagem(self.socket_udp)
            self.page.run_task(self._processar_mensagem_pauta, mensagem_servidor)
        except Exception as e:
            print(f"Erro ao aguardar pauta inicial: {e}")
            self.page.run_task(self._navegar_assincrono, "/")

    def entrar_na_votacao_como_votante(self, e: ft.ControlEvent) -> None:
        self.page.go("/atencao_votante")

    def iniciar_escuta_votante(self, e: ft.ControlEvent) -> None:

        self.socket_udp = cliente.virar_votante()
        self.page.go("/aguardar_host")
        thread_de_espera = Thread(target=self._tarefa_esperar_pauta, daemon=True)
        thread_de_espera.start()

    def votar(self, e: ft.ControlEvent) -> None:
        if e.control.data == 2:
            self.voto_pendente = "A favor"
        elif e.control.data == 1:
            self.voto_pendente = "Contra"
        elif e.control.data == 0:
            self.voto_pendente = "Abster-se"
        self.page.go("/confirmacao")

    def confirmar_voto(self, e: ft.ControlEvent) -> None:
        cliente.votar(self.socket_udp, self.voto_pendente, self.mensagem)
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
            self.socket_udp = socket_host
            self.host_ativo = True
            self.banco_de_dados, self.processo_de_escuta, self.flag_de_controle = (
                servidor.aguardar_votantes(self.socket_udp)
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
        self.processo_de_escuta.join()
        self.page.go("/criacao_de_pauta")

    def enviar_pauta(self, e: ft.ControlEvent) -> None:
        if self.timer_encerramento and self.timer_encerramento.is_alive():
            self.timer_encerramento.cancel()

        self.processo_de_escuta, self.flag_de_controle = servidor.aguardar_votos(
            self.banco_de_dados, self.socket_udp
        )
        campo_pauta, dropdown_tempo = e.control.data
        pauta_texto = campo_pauta.value
        tempo_selecionado = int(dropdown_tempo.value)
        self.mensagem = pauta_texto
        self.banco_de_dados.adicionar_pauta(self.mensagem)
        self.banco_de_dados.serializar_dados()
        mensagem_com_tempo = f"{self.mensagem}|{tempo_selecionado}"
        servidor.mandar_mensagem(
            self.banco_de_dados, self.socket_udp, mensagem_com_tempo
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
            self.processo_de_escuta.join()
            self.resultado_votacao = servidor.mostrar_resultados(
                self.banco_de_dados, self.socket_udp, self.mensagem, enviar=False
            )
            self.page.go("/resultado_host_intermediario")

    def enviar_resultado_para_votantes(self, e: ft.ControlEvent) -> None:

        if self.resultado_votacao:
            servidor.mandar_mensagem(
                self.banco_de_dados, self.socket_udp, self.resultado_votacao
            )

        caixa_de_dialogo = ft.AlertDialog(
            title=ft.Text("Resultado enviado com sucesso!"), modal=True
        )
        self.page.dialog = caixa_de_dialogo
        caixa_de_dialogo.open = True
        self.page.update()

        time.sleep(2)
        caixa_de_dialogo.open = False
        self.page.go("/resultado_host_final")
        self.page.update()

    def criar_nova_pauta(self, e):
        self.pauta_string = None
        self.tempo_pauta = None

        servidor.mandar_mensagem(
            self.banco_de_dados, self.socket_udp, "host_criando_nova_pauta"
        )

        self.page.go("/criacao_de_pauta")

    def encerrar_sessao(self, e: ft.ControlEvent) -> None:
        self.mensagem = "sessao encerrada"
        servidor.mandar_mensagem(self.banco_de_dados, self.socket_udp, self.mensagem)
        self.host_ativo = False
        self._limpar_recursos()
        self.page.go("/")

    def _limpar_recursos(self):

        print("--- APP ENCERRANDO: REALIZANDO A LIMPEZA ---")
        if hasattr(self, "flag_de_controle") and self.flag_de_controle:
            self.flag_de_controle.set()

        if hasattr(self, "socket_udp") and self.socket_udp:
            self.socket_udp.close()
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