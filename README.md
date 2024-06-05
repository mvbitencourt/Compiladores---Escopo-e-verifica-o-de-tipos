# Gerenciamento de Escopo e Verificação de Tipos em um Compilador

Este projeto implementa o gerenciamento de escopo e a verificação de tipos para uma linguagem fictícia simplificada que suporta atribuições de valores e criação de escopos. A funcionalidade principal inclui a manutenção de uma tabela de símbolos para rastrear variáveis e seus escopos, verificar a compatibilidade de tipos e lidar com vários construtos da linguagem, como blocos, declarações de variáveis e comandos de impressão.

## Arquivos no Projeto

- `escopo1.txt`: Um arquivo de entrada de exemplo com escopos aninhados e declarações de variáveis.
- `escopo2.txt`: Outro arquivo de entrada de exemplo demonstrando diferentes cenários de escopo.
- `escopo3.txt`: Arquivo de entrada adicional com estruturas de escopo complexas.
- `gerenciados_de_escopos.py`: O script Python principal que implementa a lógica de gerenciamento de escopo e verificação de tipos.
- `saida.txt`: Arquivo de saída onde os resultados do script são escritos.

## Script Python: `gerenciados_de_escopos.py`

Este script lê um arquivo de entrada contendo código na linguagem fictícia, processa-o para gerenciar escopos e tipos, e escreve os resultados em um arquivo de saída. Abaixo está uma visão geral das funções principais e da lógica implementada no script.

### Funções Principais

1. **Dicionário de Expressões Regulares (`ER_DICIONARIO`)**
    - Contém expressões regulares para diferentes construtos da linguagem, como início/fim de bloco, tipos de variáveis, identificadores, números e literais de string.

2. **Lista de Tokens (`tokens`)**
    - Mapeia tokens para suas expressões regulares correspondentes.

3. **Verificação de Tokens (`verifica_token_linha`)**
    - Determina o tipo de token para uma determinada linha de código usando as expressões regulares.

4. **Extração de Variáveis e Valores (`extrair_variaveis_tipos_valores_declaracao`, `extrair_valor_variavel_atribuicao`)**
    - Extrai tipos de variáveis, nomes e valores de linhas de declaração e atribuição.

5. **Gerenciamento de Escopo (`verificar_declaracao_no_escopo_atual`, `atribuir_valor_variavel`)**
    - Gerencia declarações de variáveis e atribuições dentro do escopo atual.

6. **Loop Principal de Processamento (`main`)**
    - Lê o arquivo de entrada linha por linha, processa cada linha de acordo com seu tipo de token, gerencia escopos, atualiza a tabela de símbolos e escreve os resultados no arquivo de saída.
