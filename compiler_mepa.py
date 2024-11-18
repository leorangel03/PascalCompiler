import re

# Lista de palavras reservadas na linguagem PascalLite
palavras_reservadas = [
    'begin', 'boolean', 'div', 'do', 'else', 'end', 'false', 
    'if', 'integer', 'mod', 'program', 'read', 'then', 
    'true', 'not', 'var', 'while', 'write'
]

# Dicionário de operadores e seus tokens correspondentes
mapa_operadores = {
    '+': 'SOMA',
    '-': 'SUB',
    '*': 'MULT',
    '/': 'DIV',
    ':=': 'ATRIB',
    '>': 'MAIOR',
    '<': 'MENOR',
    '<=': 'MENOR_IGUAL',
    '>=': 'MAIOR_IGUAL',
    '=': 'IGUAL',
    '<>': 'DIFERENTE'
}

# Dicionário de pontuações e seus tokens correspondentes
mapa_pontuacoes = {
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

# Classe para gerenciar a tabela de símbolos
class TabelaDeSimbolos:
    def __init__(self):
        self.simbolos = {}
        self.proximo_endereco = 0

    def adicionar_variavel(self, nome, tipo):
        """Adiciona uma variável na tabela de símbolos."""
        if nome in self.simbolos:
            raise Exception(f"Erro: Variável '{nome}' já declarada.")
        self.simbolos[nome] = {'endereco': self.proximo_endereco, 'tipo': tipo}
        self.proximo_endereco += 1

    def buscar_variavel(self, nome):
        """Busca uma variável na tabela de símbolos."""
        if nome not in self.simbolos:
            raise Exception(f"Erro: Variável '{nome}' não declarada.")
        return self.simbolos[nome]['endereco']

# Função para gerar rótulos únicos
rotulo_atual = 0

def gerar_rotulo():
    """Gera um rótulo único."""
    global rotulo_atual
    rotulo_atual += 1
    return f"L{rotulo_atual}"

# Classe para o analisador léxico
class AnalisadorLexico:
    def __init__(self, codigo_fonte):
        self.codigo_fonte = codigo_fonte
        self.tokens = []
        self.linhas = codigo_fonte.split('\n')
        self.tokenizar()

    def tokenizar(self):
        """Divide o código em tokens usando expressões regulares."""
        padroes_tokens = [
            ('COMENTARIO', r'{[^}]*}|(\(\*[^*]*\*\))|(//.*)'),
            ('IDENTIFICADOR', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('NUMERO', r'\d+'),
            ('OPERADOR', r'(\+|-|\*|\/|:=|=|<>|<=|>=|<|>)'),
            ('PONTUACAO', r'[.,;:()\[\]{}]'),
            ('NOVA_LINHA', r'\n'),
            ('DELIMITADOR', r'[ \t]+'),
            ('FIM_ARQUIVO', r'\0'),
            ('ERRO', r'.')
        ]
        
        regex_completa = '|'.join(f'(?P<{nome}>{padrao})' for nome, padrao in padroes_tokens)
        
        for linha_idx, linha in enumerate(self.linhas):
            for correspondencia in re.finditer(regex_completa, linha):
                tipo = correspondencia.lastgroup
                lexema = correspondencia.group()
                
                if tipo in ['NOVA_LINHA', 'DELIMITADOR', 'COMENTARIO']:
                    continue
                elif tipo == 'IDENTIFICADOR' and lexema in palavras_reservadas:
                    tipo = lexema.upper()
                elif tipo == 'OPERADOR':
                    tipo = mapa_operadores.get(lexema, 'OPERADOR')
                elif tipo == 'PONTUACAO':
                    tipo = mapa_pontuacoes.get(lexema, 'PONTUACAO')
                
                self.tokens.append((tipo, lexema, linha_idx + 1))

    def proximo_token(self):
        """Retorna o próximo token ou None se não houver mais."""
        return self.tokens.pop(0) if self.tokens else None

# Classe para gerar instruções MEPA
class GeradorInstrucoesMEPA:
    def __init__(self, analisador_lexico):
        self.lexico = analisador_lexico
        self.tabela_simbolos = {}
        self.endereco_atual = 0
        self.instrucoes = []
        self.processar_tokens()

    def processar_tokens(self):
        """Processa os tokens gerados pelo analisador léxico."""
        token = self.lexico.proximo_token()
        while token:
            tipo, lexema, linha = token
            if tipo == 'PROGRAM':
                self.instrucoes.append("INPP")
            elif tipo == 'IDENTIFICADOR':
                self.processar_identificador(lexema)
            elif tipo == 'NUMERO':
                self.instrucoes.append(f"CRCT {lexema}")
            elif tipo == 'ATRIB':
                self.instrucoes.append("ARMZ 0")
            elif tipo == 'READ':
                self.instrucoes.append("LEIT")
            elif tipo == 'WRITE':
                self.instrucoes.append("IMPR")
            elif tipo == 'BEGIN':
                self.instrucoes.append("INICIO")
            elif tipo == 'END':
                self.instrucoes.append("PARA")
            token = self.lexico.proximo_token()

    def processar_identificador(self, lexema):
        """Trata identificadores."""
        if lexema not in self.tabela_simbolos:
            self.tabela_simbolos[lexema] = self.endereco_atual
            self.endereco_atual += 1
        self.instrucoes.append(f"CRVL {self.tabela_simbolos[lexema]}")

    def gerar_instrucoes(self):
        """Retorna todas as instruções geradas."""
        return "\n".join(self.instrucoes)

# Função para ler o arquivo de código fonte
def leia_arquivo():
    caminho_arquivo = 'testes cods/teste4.txt'  # Atualize o nome para outros testes
    with open(caminho_arquivo, 'r') as arquivo:
        return arquivo.read()

# Função principal
def main():
    """Ponto de entrada principal do programa."""
    codigo_fonte = leia_arquivo()  # Lê o código do arquivo
    analisador_lexico = AnalisadorLexico(codigo_fonte)  # Instancia o analisador léxico
    
    # Geração das instruções MEPA
    gerador_mepa = GeradorInstrucoesMEPA(analisador_lexico)
    instrucoes_mepa = gerador_mepa.gerar_instrucoes()
    
    # Imprime as instruções MEPA
    print(instrucoes_mepa)
    print('-' * 40)  # Linha separadora

# Chamada da função principal
main()

