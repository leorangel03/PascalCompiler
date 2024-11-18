# PascalCompiler

Projeto realizado na FIT, proposto pelo professor Leonardo Massayuki Takuno, para a fixação do conteudo do semestre. Consiste na implementação de um analisador léxico e sintático em Python para a linguagem simplificada **PascalLite**. O projeto identifica tokens, valida a estrutura do código-fonte e gera instruções para a Máquina de Execução Paralela Abstrata (MEPA).


## Estrutura do Projeto

O projeto contém duas principais classes:

1. **Analisador_Lexico**: Responsável pela análise léxica do código fonte, identificando e gerando os átomos (tokens) a partir do texto.
2. **AnalisadorSintatico**: Realiza a análise sintática, verificando se a sequência de tokens gerados pelo analisador léxico está de acordo com as regras gramaticais da linguagem.
3. **TabelaDeSimbolos**: Gerencia a tabela de símbolos, armazenando variáveis e seus atributos como endereço e tipo.
4. **GeradorInstrucoesMEPA**: Traduz os tokens gerados pelo analisador léxico em instruções MEPA.

### Principais Componentes

- **Atomo**: Classe que representa um token, contendo seu tipo, lexema e a linha em que foi encontrado.
- **Dicionários**:
  - `operadores_dict`: Mapeia operadores para seus identificadores.
  - `pontuacoes_dict`: Mapeia pontuações para seus identificadores.
- **Lista de Palavras Reservadas**: Contém palavras-chave da linguagem PascalLite.
- **Palavras Reservadas**: Contém palavras-chave da linguagem PascalLite, como `begin`, `end`, `program`, entre outras.
- **Mapeamento de Operadores e Pontuações**: Dicionários que associam símbolos aos seus respectivos tokens, como `+` para `SOMA` e `;` para `PONTO_VIRG`.
- **Geração de Rótulos**: Uma função auxiliar gera rótulos únicos utilizados nas instruções MEPA.


### Tokens

Os tokens gerados incluem:

- **Palavras Reservadas**: `PROGRAM`, `BEGIN`, `END`, etc.
- **IDENTIFICADOR**: Nomes de variáveis e funções.
- **NUMERO**: Constantes numéricas.
- **OPERADOR**: Operadores aritméticos e lógicos como `+`, `-`, `*`, `=`, etc.
- **PONTUACAO**: Pontuações como `;`, `,`, `:`, `(`, `)`.
- **COMENTARIO**: Comentários no código.
- **DELIMITADOR**: Espaços e tabulações.
- **ERRO**: Caracteres não reconhecidos.

### Funções Principais

- **leia_arquivo**: Lê o código fonte de um arquivo especificado.
- **main**: Função principal que coordena a leitura do arquivo, a análise léxica e sintática, e exibe os resultados.

### Instruções MEPA
Durante o processamento, o código gera instruções para a MEPA, como:

- **INPP**: Inicializa o programa.
- **CRCT**: Carrega uma constante.
- **ARMZ**: Armazena o valor em uma variável.
- **LEIT**: Realiza a leitura de uma variável.
- **IMPR**: Imprime valores.
- **PARA**: Finaliza o programa.

## Uso

1. Altere o nome do arquivo na função `leia_arquivo` para o arquivo de código que você deseja analisar.
2. Execute o código. O analisador irá ler o arquivo, gerar tokens e verificar a estrutura do código.
3. Se a análise for bem-sucedida, será exibida a mensagem "Análise sintática concluída com sucesso!". Caso contrário, erros sintáticos serão exibidos.
4. Execute o programa. As instruções MEPA serão exibidas no console.
5. Utilize os exemplos na pasta `testes cods` para verificar o funcionamento.
