import flet as ft
from servidor import servidor, cliente
import threading
import time

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

        self.tempo_votacao = 0
        self.timer_control_votante = None
        self.timer_thread_votante = None
        self.stop_timer_event = threading.Event()
        
        self.pauta_start_timestamp = None 
        self.current_pauta_text = None 

        print(f"[Controlador INIT]: pauta_start_timestamp={self.pauta_start_timestamp}, current_pauta_text={self.current_pauta_text}")
        self.page.go('/')

    def entrar_na_votacao_como_votante(self, e) -> None:
        self.udp_socket = cliente.virar_votante()
        self.page.go('/espera')

        mensagem_recebida = cliente.receber_mensagem(self.udp_socket)

        self.stop_voter_countdown() 
        print(f"[entrar_na_votacao_como_votante]: stop_voter_countdown called.")

        if mensagem_recebida == 'votação encerrada':
            self.mensagem = "A votação geral foi encerrada pelo Host."
            if self.page.route == '/espera' or self.page.route == '/votacao':
                 self.page.go('/resultado')
            print(f"[entrar_na_votacao_como_votante]: Votação encerrada recebida. Indo para /resultado.")
            return

        try:
            partes = mensagem_recebida.split('|', 1)
            if len(partes) == 2:
                nova_pauta_texto = partes[0]
                novo_tempo_votacao = int(partes[1])

                if nova_pauta_texto != self.current_pauta_text:
                    self.current_pauta_text = nova_pauta_texto
                    self.pauta_start_timestamp = time.time()
                    self.tempo_votacao = novo_tempo_votacao
                    self.mensagem = nova_pauta_texto
                    print(f"[entrar_na_votacao_como_votante]: NOVA PAUTA '{nova_pauta_texto}'. pauta_start_timestamp set to {self.pauta_start_timestamp}")
                else:
                    print(f"[entrar_na_votacao_como_votante]: MESMA PAUTA '{nova_pauta_texto}'. pauta_start_timestamp={self.pauta_start_timestamp} (não resetado).")

                self.mensagem = nova_pauta_texto
                self.tempo_votacao = novo_tempo_votacao

                if self.page.route == '/espera':
                    print(f"[entrar_na_votacao_como_votante]: Indo para /votacao.")
                    self.page.go('/votacao')
            else:
                print(f"[entrar_na_votacao_como_votante]: AVISO: Formato inesperado da mensagem da pauta: '{mensagem_recebida}'")
                self.mensagem = mensagem_recebida
                self.tempo_votacao = 0
                
                if "Resultado da votação" in self.mensagem:
                     if self.page.route == '/espera': self.page.go('/resultado')
                     print(f"[entrar_na_votacao_como_votante]: Mensagem é resultado. Indo para /resultado.")
                elif self.page.route == '/espera':
                    self.page.go('/votacao')
                    print(f"[entrar_na_votacao_como_votante]: Mensagem desconhecida, mas indo para /votacao.")

        except ValueError:
            print(f"[entrar_na_votacao_como_votante]: ERRO: Não foi possível extrair o tempo da mensagem da pauta: '{mensagem_recebida}'")
            self.mensagem = "Erro ao carregar pauta. Verifique a mensagem do servidor."
            self.tempo_votacao = 0
            if self.page.route == '/espera':
                 self.page.go('/votacao')
        except Exception as ex:
            print(f"[entrar_na_votacao_como_votante]: ERRO: Erro inesperado ao processar mensagem da pauta: {ex}")
            self.mensagem = "Erro inesperado ao processar mensagem da pauta."
            self.tempo_votacao = 0
            if self.page.route == '/espera':
                 self.page.go('/votacao')

    def start_voter_countdown(self):
        print(f"[start_voter_countdown]: Chamado. pauta_start_timestamp atual={self.pauta_start_timestamp}, tempo_votacao={self.tempo_votacao}")
        if not self.timer_control_votante or self.tempo_votacao <= 0 or self.pauta_start_timestamp is None:
            print(f"[start_voter_countdown]: Não iniciando. timer_control_votante={self.timer_control_votante}, tempo_votacao={self.tempo_votacao}, pauta_start_timestamp={self.pauta_start_timestamp}")
            if self.timer_control_votante and self.tempo_votacao <= 0 :
                 self.timer_control_votante.value = "Tempo não definido."
            elif self.timer_control_votante and self.pauta_start_timestamp is None:
                 self.timer_control_votante.value = "Aguardando início do tempo..."
            try:
                self.page.update()
            except: pass
            return

        print(f"[start_voter_countdown]: Parando thread antiga (se houver).")
        self.stop_voter_countdown() 

        self.stop_timer_event.clear()
        
        print(f"[start_voter_countdown]: Iniciando NOVA thread do timer. pauta_start_timestamp={self.pauta_start_timestamp}")
        self.timer_thread_votante = threading.Thread(target=self._voter_countdown_task, daemon=True)
        self.timer_thread_votante.start()

    def _voter_countdown_task(self):
        thread_id = threading.get_ident()
        print(f"[_voter_countdown_task {thread_id}]: Thread iniciada. pauta_start_timestamp={self.pauta_start_timestamp}")

        if self.pauta_start_timestamp is None:
            current_time = self.tempo_votacao
            print(f"[_voter_countdown_task {thread_id}]: AVISO: pauta_start_timestamp é None. Usando tempo_votacao como fallback.")
        else:
            elapsed_time = int(time.time() - self.pauta_start_timestamp)
            current_time = max(0, self.tempo_votacao - elapsed_time)
            print(f"[_voter_countdown_task {thread_id}]: Tempo inicial calculado: {current_time}s (tempo_votacao={self.tempo_votacao}, decorrido={elapsed_time})")
        
        while current_time >= 0 and not self.stop_timer_event.is_set():
            if self.page.route != "/votacao" and self.page.route != "/confirmacao":
                print(f"[_voter_countdown_task {thread_id}]: Rota mudou para {self.page.route}. Saindo do loop.")
                break

            if self.timer_control_votante:
                if current_time > 0:
                    new_value = f"Tempo restante: {current_time}s"
                else:
                    new_value = "Tempo esgotado!"
                
                if self.timer_control_votante.value != new_value:
                    self.timer_control_votante.value = new_value
                    try:
                        self.page.update()
                    except Exception as e:
                        print(f"[_voter_countdown_task {thread_id}]: Falha na atualização da UI: {e}. Parando thread.")
                        self.stop_timer_event.set()
                        break
            
            if current_time == 0:
                print(f"[_voter_countdown_task {thread_id}]: current_time chegou a 0. Saindo do loop.")
                break

            time.sleep(1)
            
            if self.pauta_start_timestamp is not None:
                elapsed_time = int(time.time() - self.pauta_start_timestamp)
                current_time = max(0, self.tempo_votacao - elapsed_time)
            else:
                current_time -= 1
                print(f"[_voter_countdown_task {thread_id}]: pauta_start_timestamp é None no loop. Decrementando manualmente.")

        print(f"[_voter_countdown_task {thread_id}]: Thread finalizada.")

    def stop_voter_countdown(self):
        print(f"[stop_voter_countdown]: Chamado. Sinalizando stop_timer_event.")
        self.stop_timer_event.set()
        if self.timer_thread_votante and self.timer_thread_votante.is_alive():
            thread_id = self.timer_thread_votante.ident
            print(f"[stop_voter_countdown]: Aguardando thread {thread_id} terminar...")
            self.timer_thread_votante.join(timeout=1.0)
            if self.timer_thread_votante.is_alive():
                print(f"[stop_voter_countdown]: AVISO! Thread {thread_id} NÃO terminou graciosamente após join.")
        self.timer_thread_votante = None
        print(f"[stop_voter_countdown]: Referência da thread limpa.")

    def votar(self, e: ft.ControlEvent):
        if e.control.data == 2:
            self.voto_pendente = 'a favor'
        elif e.control.data == 1:
            self.voto_pendente = 'contra'
        elif e.control.data == 0:
            self.voto_pendente = 'nulo'
        print(f"[votar]: Navegando para /confirmacao. Voto pendente: {self.voto_pendente}")
        self.page.go('/confirmacao')

    def confirmar_voto(self, e):
        print(f"[confirmar_voto]: Parando cronômetro do votante.")
        self.stop_voter_countdown() 
        try:
            cliente.votar(self.udp_socket, self.voto_pendente, self.mensagem)
            self.page.go('/espera')
            
            mensagem_resultados = cliente.receber_mensagem(self.udp_socket)
            self.mensagem = mensagem_resultados

            if "Resultado da votação" in self.mensagem or self.mensagem == 'votação encerrada':
                print(f"[confirmar_voto]: Mensagem de resultado ou votação encerrada. Indo para /resultado.")
                self.pauta_start_timestamp = None 
                self.current_pauta_text = None
                self.page.go('/resultado')
            else:
                print(f"[confirmar_voto]: Nova pauta recebida após voto. Re-entrando no fluxo do votante.")
                self.entrar_na_votacao_como_votante(None) 
                return

        except Exception as ex:
            print(f"[confirmar_voto]: ERRO: {ex}")
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao confirmar voto ou receber resultado: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()
            self.page.go('/')
            return

    def cancelar_voto(self, e):
        print(f"[cancelar_voto]: Parando cronômetro do votante.")
        self.stop_voter_countdown()
        print(f"[cancelar_voto]: Navegando para /votacao.")
        self.page.go('/votacao')

    def encerrar_espera_de_votos(self, e):
        self.flag_de_controle.set()
        self.process.join()
        self.mensagem = servidor.mostrar_resultados(self.banco_de_dados, self.udp_socket, self.mensagem)
        self.page.go('/resultado')

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
        tempo = int(dropdown_tempo.value)

        self.banco_de_dados.adicionar_pauta(self.mensagem)
        self.banco_de_dados.serializar_dados()
        
        mensagem_com_tempo = f"{self.mensagem}|{tempo}"
        servidor.mandar_mensagem(self.banco_de_dados, self.udp_socket, mensagem_com_tempo)

        def encerrar_votacao_automaticamente():
            if not self.flag_de_controle.is_set():
                async def _async_encerrar_espera_de_votos():
                    self.encerrar_espera_de_votos(None)
                
                self.page.run_task(_async_encerrar_espera_de_votos)

        threading.Timer(tempo, encerrar_votacao_automaticamente).start()

        self.page.go('/espera_votos')