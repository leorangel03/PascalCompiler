#------------------------------ IMPORTAÇÃO DE LIB, CRIAÇÃO DE ESTRUTURAS, PADROES E CLASSE DO ATOMO ------------------------------
import re
from typing import NamedTuple

# dict para nomear os atomos
operadores_dict = {
    '+': 'OP_SOMA',
    '-': 'OP_SUB',
    '*': 'OP_MULT',
    '/': 'OP_DIVREAL',
    ':=': 'ATRIB',
    '>': 'MAIOR',
    '<': 'MENOR',
    '<=': 'MENOR_IGUAL',
    '>=': 'MAIOR_IGUAL',
    '=': 'IGUAL',
    '<>': 'DIFERENTE'
}
# dict para nomear os atomos
pontuacoes_dict = {
    ',': 'VIRGULA',
    ';': 'PONTO_VIRG',
    '.': 'PONTO',
    ':': 'DOIS_PONTOS',
    '(': 'PAR_ABRE',
    ')': 'PAR_FECHA',
    '[': 'COLCHETE_ABRE',
    ']': 'COLCHETE_FECHA',
    '{': 'CHAVE_ABRE',
    '}': 'CHAVE_FECHA'
}
#lista de palavras reservadas
palavras_reservada = ['begin', 'boolean', 'div', 'do', 'else', 'end', 'false', 'if', 'integer', 'mod', 'program', 'read', 'then',
                       'true', 'not', 'var', 'while','write']
# lista com os tokens para a linguaugem
token_def = [
    ('COMENTARIO', r'{[^}]*}|(\(\*[^*]*\*\))|(//.*)'), 
    ('IDENTIF', '[a-zA-Z_][a-zA-Z0-9_]*'),
    ('NUMERO', '\\d+(\\.\\d*)?'),
    ('OPERADOR', r'(\+|-|\*|\/|:=|=|<>|<=|>=|<|>)'),    
    ('PONTUACAO', r'[.,;:()\[\]{}]'),    
    ('NOVA_LINHA', '\n'),    
    ('DELIMITADOR', '[ \t]+'),    
    ('EOS', '\0'),    
    ('ERRO', '.')
    ]

tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_def)# Padrao para as lista de token

class Atomo(NamedTuple):# criando a classe atomo com as 3  variaveis
    tipo: str
    lexema: str
    linha: int

#------------------------------ INICIO DO ANALISADOR LÉXICO ------------------------------
class ErroLexicoException(Exception):
  pass

class Analisador_Lexico:
    def __init__(self, buffer): #metodo principal contendo o buffer e o match object
        self.buffer = buffer #pega o buffer do arquivo do main
        self.match_object = self.obter_atomos()#chamando o metodo obter atomos

    def obter_atomos(self):
        linha = 1
        for tok in re.finditer(tok_regex, self.buffer):#percorre todos os tokens encontrados na string self.buffer
            tipo = tok.lastgroup
            lexema = tok.group()
            if tipo == 'NOVA_LINHA':# Itera uma nova linha
                linha += 1
                continue
            elif tipo == 'DELIMITADOR':# Ignora delimitadores
                continue
            elif tipo == 'COMENTARIO':# Ignora comentários
                linhas_comentario = lexema.count('\n')# conta quantas linhas tiveram o comentario
                linha += linhas_comentario
                continue
            elif tipo == 'IDENTIF':# VERIFICO SE O IDENTIFICADOR ESTA NA LISTA DE PALAVRAS RESERVADAS
                if len(lexema) > 20:
                    print(f'Linha: {linha:02d} - ERRO LÉXICO: "{lexema}" IDENTIFICADOR MUITO LONGO')
                    exit(1)
                if lexema in palavras_reservada:
                    tipo = lexema.upper()# Pode usar o lexema como o tipo (ex: BEGIN, END)
                else:
                    tipo = 'IDENTIF'
            elif tipo == 'NUMERO':# Definições específicas para numeros
                tipo = 'NUM_REAL' if '.' in lexema else 'NUM_INT'
            elif tipo == 'OPERADOR':# Definições específicas para operadores
                    tipo = operadores_dict.get(lexema, 'OPERADOR')
            elif tipo == 'PONTUACAO':# Definições específicas para pontuações
                tipo = pontuacoes_dict.get(lexema, 'PONTUAÇÃO')
            elif tipo == 'ERRO':# Identifica ERRO e trata exeção
                print(f'Linha: {linha:02d} - ERRO LÉXICO: "{lexema}"')

            yield Atomo(tipo, lexema, linha) # Produz um atomo a cada iteração do for sem sair do laço
    
    def proximo_atomo(self):# metodo para pegar o proximo atomo através do matcobject e tratando exeçao no final da itereção
        try:
            return next(self.match_object)
        except StopIteration:
            return Atomo('EOS', '', 0)
        
#------------------------------ INICIO DO ANALISADOR SINTATICO ------------------------------
class ErroSintaticoException(Exception):
    pass

class AnalisadorSintatico:
    def __init__(self, analisador_lexico):
        self.lex = analisador_lexico #cria o lex
        self.atomo_atual = self.lex.proximo_atomo() #instancia o atomo_atual do proximo atomo para as verificacoes do sintatico

    def consome(self, tipo_esperado):#crio o metodo consome atomo caso diferente do esperado da erro
        if self.atomo_atual.tipo == tipo_esperado:
            print(f'Linha: {self.atomo_atual.linha:02d} - atomo: {self.atomo_atual.tipo.ljust(15)} lexema: {self.atomo_atual.lexema.ljust(15)}')
            self.atomo_atual = self.lex.proximo_atomo()
        else:
            raise ErroSintaticoException(f"Erro sintático: esperado {tipo_esperado}, mas encontrou {self.atomo_atual.tipo}")

    def programa(self):#1º sintaxe do programa
        self.consome('PROGRAM')
        self.consome('IDENTIF')
        self.consome('PONTO_VIRG')
        self.bloco()
        self.consome('PONTO')

    def bloco(self):#2º estrutura do bloco de variaveis
        self.declaracao_variaveis()
        self.comando_composto()

    def declaracao_variaveis(self):#sintaxe da delcaracao de variavel
        if self.atomo_atual.tipo == 'VAR':
            self.consome('VAR')
            while self.atomo_atual.tipo == 'IDENTIF':
                self.lista_identificadores()
                self.consome('DOIS_PONTOS')
                self.tipo()
                self.consome('PONTO_VIRG')

    def lista_identificadores(self):#lista de variaveis caso haja mais de uma
        self.consome('IDENTIF')
        while self.atomo_atual.tipo == 'VIRGULA':
            self.consome('VIRGULA')
            self.consome('IDENTIF')

    def tipo(self):# verifica tipo da variavel
        if self.atomo_atual.tipo in ['INTEGER', 'BOOLEAN']:
            self.consome(self.atomo_atual.tipo)
        else:
            raise ErroSintaticoException(f"Erro sintático: tipo inválido {self.atomo_atual.tipo}")

    def comando_composto(self):#3º estrutura dos comandos entre begin -> end
        self.consome('BEGIN')
        self.lista_comandos()
        self.consome('END')

    def lista_comandos(self):#estrutura caso haja mais de um comando
        self.comando()  # Processa o primeiro comando
        while self.atomo_atual.tipo == 'PONTO_VIRG':
            self.consome('PONTO_VIRG')  # Consome o ponto e vírgula
            if self.atomo_atual.tipo == 'END':# Verifica se o próximo token é END
                break  # Para se encontrar END, pois não há mais comandos
            self.comando()  # Processa o próximo comando
        if self.atomo_atual.tipo != 'END':# Verifica se o token atual não é END, e gera um erro sintático
            raise ErroSintaticoException(f"Erro sintático: esperado 'END', mas encontrou {self.atomo_atual.tipo}")

    def comando(self):#tipos de comando
        if self.atomo_atual.tipo == 'IDENTIF':
            self.atribuicao()
        elif self.atomo_atual.tipo == 'READ':
            self.comando_entrada()
        elif self.atomo_atual.tipo == 'WRITE':
            self.comando_saida()
        elif self.atomo_atual.tipo == 'IF':
            self.comando_if()
        elif self.atomo_atual.tipo == 'WHILE':
            self.comando_while()
        else:
            raise ErroSintaticoException(f"Erro sintático: comando inválido: {self.atomo_atual.tipo}")

    def atribuicao(self):#comando para atribuicao de variavel
            self.consome('IDENTIF')
            self.consome('ATRIB')
            self.expressao()

    def comando_saida(self):#comando para saida de valores
        self.consome('WRITE')
        self.consome('PAR_ABRE')
        self.expressao()
        self.consome('PAR_FECHA')

    def comando_entrada(self):#comando para entrada de valores
        self.consome('READ')
        self.consome('PAR_ABRE')
        self.lista_identificadores()  # Atualização para lidar com múltiplos identificadores
        self.consome('PAR_FECHA')

    def comando_if(self):#comando para a estrutura if
        self.consome('IF')  # Consome o token IF
        self.expressao()  # Processa a expressão da condição
        self.consome('THEN')  # Espera pelo token THEN
        if self.atomo_atual.tipo == 'BEGIN':# Verifica se há um bloco de comandos
            self.consome('BEGIN')  # Consome o token BEGIN
            self.lista_comandos()  # Processa os comandos dentro do bloco
            self.consome('END')  # Consome o token END
        else:
            self.comando()  # Caso contrário, apenas consome um único comando
        if self.atomo_atual.tipo == 'ELSE':# Verifica se há um bloco ELSE
            self.consome('ELSE')  # Consome o token ELSE
            if self.atomo_atual.tipo == 'BEGIN':# Verifica se há um bloco de comandos após o ELSE
                self.consome('BEGIN')  # Consome o token BEGIN
                self.lista_comandos()  # Processa os comandos do bloco ELSE
                self.consome('END')  # Consome o token END
            else:
                self.comando()  # Caso contrário, apenas consome um único comando

    def comando_while(self):#comando para a estrutura if
        self.consome('WHILE')  # Consume o token WHILE
        self.expressao()  # Avalia a condição do loop
        self.consome('DO')  # Consume o token DO
        if self.atomo_atual.tipo == 'BEGIN':
            self.comando_composto()  # Processa o bloco de comandos dentro do loop
        else:
            self.comando()  # Processa um único comando

    def expressao(self):# comando para expreçoes simples
        self.termo()  # Processa o primeiro termo
        while self.atomo_atual.tipo in ['OP_SOMA', 'OP_SUB']:
            self.consome(self.atomo_atual.tipo)  # Consome operador de soma ou subtração
            self.termo()  # Processa o próximo termo
        # Aqui você pode adicionar a lógica para operadores de comparação
        if self.atomo_atual.tipo in ['MAIOR', 'MENOR', 'MAIOR_IGUAL', 'MENOR_IGUAL', 'IGUAL', 'DIFERENTE']:
            self.consome(self.atomo_atual.tipo)  # Consome o operador de comparação
            self.termo()  # Processa a segunda parte da comparação

    def termo(self):#comando para mult e divisao
        self.fator()
        while self.atomo_atual.tipo in ['OP_MULT', 'OP_DIVREAL']:
            self.consome(self.atomo_atual.tipo)
            self.fator()

    def fator(self):#função o para fator
        if self.atomo_atual.tipo == 'IDENTIF':
            self.consome('IDENTIF')
        elif self.atomo_atual.tipo == 'NUM_INT':
            self.consome('NUM_INT')
        elif self.atomo_atual.tipo == 'NUM_REAL':
            self.consome('NUM_REAL')
        elif self.atomo_atual.tipo == 'PAR_ABRE':
            self.consome('PAR_ABRE')
            self.expressao()
            self.consome('PAR_FECHA')
        else:
            raise ErroSintaticoException(f"Fator inválido: {self.atomo_atual.tipo}")

#------------------------------LEITURA DE ARQUIVO E METODO PRINCIPAL------------------------------
def leia_arquivo():#função para ler o arquivo
    nome_arq = 'testes cods/teste3.txt'# MUDAR O NOME DO ARQUIVO PARA OS OUTROS TESTES
    with open(nome_arq, 'r') as arq:
        buffer = arq.read()
    return buffer
# funcao principal pega o buffer, instancia o analisador lexico -> sintatico, cria o while pra imprimir os atomos até q n seja EOS
def main():
    buffer = leia_arquivo()
    analisador_lexico = Analisador_Lexico(buffer)
    analisador_sintatico = AnalisadorSintatico(analisador_lexico)
    try:
        analisador_sintatico.programa()
        print("Análise sintática concluída com sucesso!")
    except ErroSintaticoException as e:
        print(e)
    print('-' * 40, end='\n')  # Isso também imprime uma quebra de linha
# chama  a função principal
main()