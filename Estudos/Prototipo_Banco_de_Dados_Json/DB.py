import json

class Banco_de_Dados:
    def __init__(self):
        self.dados = {'votantes':dict(), 'pautas':dict()}

    def ler_json(self):
        with open('db_testes.json', 'r') as banco_de_dados:
            self.dados = json.load(banco_de_dados)

    def adicionar_usuario(self, user_id):
        dicionario = {'votos contra' : list() , 'votos a favor' : list(), 'votos nulo' : list(), 'pautas sugeridas' : list(), 'pautas votadas' : list()}
        self.dados['votantes'][user_id] = dicionario 

    def adicionar_pauta(self, user_id, pauta):
        if(not(user_id in self.dados['votantes'])):
            return
        dicionario = {'qtd de votos a favor': 0, 'qtd de votos contra' : 0, 'qtd de votos anulados': 0}
        self.dados['pautas'][pauta] = dicionario
        self.dados['votantes'][user_id]['pautas sugeridas'].append(pauta)

    def renomear_pauta(self, nome_antigo, novo_nome):
        self.dados['pautas'][novo_nome] = self.dados['pautas'].pop(nome_antigo)

    def remover_pauta(self, pauta):
        self.dados['pautas'].pop(pauta)

    def registrar_voto(self, user_id, voto, pauta):
        if(not(user_id in self.dados['votantes'])):
            return

        if(pauta in self.dados['votantes'][user_id]['pautas votadas']):
            return
        if(voto == 'a favor'):
            self.dados['pautas'][pauta]['qtd de votos a favor'] += 1
            self.dados['votantes'][user_id]['votos a favor'].append(pauta)
            self.dados['votantes'][user_id]['pautas votadas'].append(pauta)

        elif(voto == 'contra'):
            self.dados['pautas'][pauta]['qtd de votos contra'] += 1
            self.dados['votantes'][user_id]['votos a contra'].append(pauta)
            self.dados['votantes'][user_id]['pautas votadas'].append(pauta)

        else:
            self.dados['pautas'][pauta]['qtd de votos anulados'] += 1
            self.dados['votantes'][user_id]['votos nulo'].append(pauta)
            self.dados['votantes'][user_id]['pautas votadas'].append(pauta)
        
    def serializar_dados(self):
        with open('db_testes.json', 'w') as banco_de_dados:
            json.dump(self.dados, banco_de_dados, ensure_ascii=False, indent=2)
