# Projeto: Gerenciador de Escopos e Analisador Semântico

## Descrição

Este projeto implementa um analisador semântico e gerenciador de escopos para um conjunto de comandos definidos em uma linguagem simplificada. O programa lê um arquivo de entrada contendo os comandos, analisa e executa esses comandos, gerenciando variáveis e escopos conforme necessário. Ele verifica declarações, atribuições e comandos de impressão (PRINT), reportando erros semânticos quando apropriado.

## Estrutura do Projeto

- **gerenciados_de_escopos.py**: Arquivo principal contendo a implementação do analisador.
- **escopo1.txt, escopo2.txt, escopo3.txt**: Arquivos de entrada contendo exemplos de comandos a serem analisados.
- **saida.txt**: Arquivo de saída onde são escritos os resultados e mensagens de erro.

## Pseudocódigo

### Inicializações

1. Definir dicionário de expressões regulares para identificar padrões específicos (início/fim de bloco, tipos, identificadores, números, cadeias, declarações, atribuições, comandos PRINT).
2. Definir listas de tokens de declaração e atribuição.

### Funções Auxiliares

- `converte_token_valor_para_tipo(valor, pilha)`: Converte valor para tipo de token correspondente.
- `verifica_token_linha(linha)`: Verifica qual token corresponde à linha.
- `extrair_tipo_variavel_declaracao(linha)`: Extrai tipo da variável de uma declaração.
- `extrair_tipo_variavel(variavel, pilha)`: Extrai tipo da variável a partir da pilha de escopos.
- `extrair_valor_variavel_atribuicao(linha)`: Extrai valor de uma atribuição.
- `extrair_variaveis_tipos_valores_declaracao(linha)`: Extrai variáveis, tipos e valores de uma declaração.
- `extrair_variaveis_print(linha)`: Extrai variáveis de um comando PRINT.
- `obter_valor_variavel(variavel, pilha)`: Obtém valor de uma variável.
- `obter_tipo_variavel(variavel, pilha)`: Obtém tipo de uma variável.
- `verificar_declaracao_variavel(linha, pilha)`: Verifica se uma variável foi declarada.
- `verificar_declaracao_no_escopo_atual(variavel, pilha)`: Verifica se uma variável foi declarada no escopo atual.
- `atribuir_valor_variavel(linha, pilha, token)`: Atribui valor a uma variável.
- `remover_todos_espacos(linha)`: Remove todos os espaços de uma linha.
- `imprimir_em_arquivo(cadeia, arquivo_saida, index_linha)`: Escreve uma cadeia no arquivo de saída.
- `limpar_arquivo_saida(arquivo_saida)`: Limpa o conteúdo do arquivo de saída.

### Função Principal

1. Definir `nome_arquivo` e `arquivo_saida`.
2. Inicializar `index_linha`, `pilha` e `tabela_simbolos`.
3. Limpar o conteúdo do arquivo de saída.
4. Abrir o arquivo de entrada em modo de leitura.
5. Para cada linha no arquivo:
    - Remover espaços em branco no início da linha.
    - Incrementar `index_linha`.
    - Verificar qual token corresponde à linha.
    - Se o token gerado for válido:
        - Processar início e fim de blocos, declarações, atribuições e comandos PRINT.
        - Gerenciar escopos e variáveis conforme necessário.
        - Reportar erros semânticos quando apropriado.
    - Imprimir estado atual da pilha.

## Como Executar

1. Certifique-se de ter o Python instalado.
2. Coloque os arquivos `escopo1.txt`, `escopo2.txt` e `escopo3.txt` na mesma pasta que `gerenciados_de_escopos.py`.
3. Execute o script `gerenciados_de_escopos.py`:
    ```bash
    python gerenciados_de_escopos.py
    ```
4. Verifique o arquivo `saida.txt` para os resultados e mensagens de erro.

## Exemplos de Uso

### Exemplo 1: escopo1.txt
```txt
BLOCO _principal_ 
	NUMERO a_1 = 12345, b

	BLOCO _n1_ 
		a_1=45
		b=55

		PRINT a_1
		PRINT b

		NUMERO nova=10
	FIM _n1_

	PRINT a_1
	PRINT nova
	
	BLOCO _n2_ 
		PRINT nova
		NUMERO x=42, c
		c=x
		x=90
		PRINT c
		PRINT x
	FIM _n2_

	PRINT x

	BLOCO _n3_
		PRINT nova
		CADEIA x="Nova cadeia"
		PRINT x
		BLOCO _n4_
			PRINT x
			PRINT c
			PRINT a
			PRINT a_1
			NUMERO a=81
			PRINT a
		FIM _n4_
		PRINT a
	FIM _n3_

	PRINT nova
	b=-934.0
	PRINT b
	PRINT a
	a=b
	PRINT a

FIM _principal_
