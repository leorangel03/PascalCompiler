# PascalCompiler

Projeto realizado na FIT, proposto pelo professor: Leonardo Massayuki Takuno, para AP1 onde consiste em implementar um analisador léxico e sintático em Python para a linguagem simplificada PascalLite. Ele identifica tokens e valida a estrutura do código fonte.


## Estrutura do Projeto

O projeto contém duas principais classes:

1. **Analisador_Lexico**: Responsável pela análise léxica do código fonte, identificando e gerando os átomos (tokens) a partir do texto.
2. **AnalisadorSintatico**: Realiza a análise sintática, verificando se a sequência de tokens gerados pelo analisador léxico está de acordo com as regras gramaticais da linguagem.

### Estruturas de Dados

- **Atomo**: Classe que representa um token, contendo seu tipo, lexema e a linha em que foi encontrado.
- **Dicionários**:
  - `operadores_dict`: Mapeia operadores para seus identificadores.
  - `pontuacoes_dict`: Mapeia pontuações para seus identificadores.
- **Lista de Palavras Reservadas**: Contém palavras-chave da linguagem PascalLite.

### Tokens

Os tokens reconhecidos pelo analisador léxico incluem:

- **COMENTARIO** 
- **IDENTIF**
- **NUMERO**
- **OPERADOR**
- **PONTUACAO**
- **NOVA_LINHA**
- **DELIMITADOR**
- **ERRO**

### Funções Principais

- **leia_arquivo**: Lê o código fonte de um arquivo especificado.
- **main**: Função principal que coordena a leitura do arquivo, a análise léxica e sintática, e exibe os resultados.

## Uso

1. Altere o nome do arquivo na função `leia_arquivo` para o arquivo de código que você deseja analisar.
2. Execute o código. O analisador irá ler o arquivo, gerar tokens e verificar a estrutura do código.
3. Se a análise for bem-sucedida, será exibida a mensagem "Análise sintática concluída com sucesso!". Caso contrário, erros sintáticos serão exibidos.
