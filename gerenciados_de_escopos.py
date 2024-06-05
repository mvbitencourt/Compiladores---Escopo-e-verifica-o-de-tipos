import re
import copy

# Dicionário de Expressões Regulares
ER_DICIONARIO = {
    "ER_BLOCO_INICIO": r"\s*BLOCO _\w+_",  # Corresponde ao início de um bloco com qualquer palavra e espaços no início
    "ER_BLOCO_FIM": r"\s*FIM _\w+_",       # Corresponde ao fim de um bloco com qualquer palavra e espaços no início
    "ER_TIPO_NUMERO": r"\s*NUMERO",      # Corresponde ao tipo NUMERO com espaços no início
    "ER_TIPO_CADEIA": r"\s*CADEIA",      # Corresponde ao tipo CADEIA com espaços no início
    "ER_IDENTIFICADOR": r"\s*[a-zA-Z_][a-zA-Z0-9_]*",  # Corresponde a identificadores de variáveis com espaços no início
    "ER_NUMERO": r"\s*[+-]?\d+(\.\d+)?",  # Corresponde a números inteiros ou reais com espaços no início
    "ER_CADEIA": r'\s*"([^"]*)"',         # Corresponde a cadeias de caracteres entre aspas duplas com espaços no início

    # Declarações de variáveis tipo NUMERO
    "ER_DECLARACAO_NUMERO": fr"\s*NUMERO\s*{r'[a-zA-Z_][a-zA-Z0-9_]*'}(,\s*{r'[a-zA-Z_][a-zA-Z0-9_]*'})*",  # Declaração de variáveis NUMERO sem inicialização com espaços no início
    "ER_DECLARACAO_NUMERO_INICIALIZADA": fr"\s*NUMERO\s*({r'[a-zA-Z_][a-zA-Z0-9_]*'}\s*=\s*{r'[+-]?\d+(\.\d+)?'}\s*,\s*)*{r'[a-zA-Z_][a-zA-Z0-9_]*'}\s*=\s*{r'[+-]?\d+(\.\d+)?'}",  # Declaração de variáveis NUMERO com inicialização com espaços no início

    # Declarações de variáveis tipo CADEIA
    "ER_DECLARACAO_CADEIA": fr"\s*CADEIA\s*{r'[a-zA-Z_][a-zA-Z0-9_]*'}(,\s*{r'[a-zA-Z_][a-zA-Z0-9_]*'})*",  # Declaração de variáveis CADEIA sem inicialização com espaços no início
    "ER_DECLARACAO_CADEIA_INICIALIZADA": fr"\s*CADEIA\s*({r'[a-zA-Z_][a-zA-Z0_]*'}\s*=\s*{r'\"([^"]*)\"'}\s*,\s*)*{r'[a-zA-Z_][a-zA-Z0_]*'}\s*=\s*{r'\"([^"]*)\"'}",  # Declaração de variáveis CADEIA com inicialização com espaços no início

    # Atribuições de variáveis
    "ER_ATRIBUICAO_NUMERO": fr"\s*{r'[a-zA-Z_][a-zA-Z0-9_]*'}\s*=\s*{r'[+-]?\d+(\.\d+)?'}",  # Atribuição de um número a uma variável com espaços no início
    "ER_ATRIBUICAO_CADEIA": fr"\s*{r'[a-zA-Z_][a-zA-Z0-9_]*'}\s*=\s*{r'\"([^"]*)\"'}",  # Atribuição de uma cadeia a uma variável com espaços no início
    "ER_ATRIBUICAO_VARIAVEL": fr"\s*{r'[a-zA-Z_][a-zA-Z0-9_]*'}\s*=\s*{r'[a-zA-Z_][a-zA-Z0-9_]*'}",  # Atribuição de uma variável a outra variável com espaços no início

    # Comandos PRINT
    "ER_PRINT": fr"\s*PRINT\s*{r'[a-zA-Z_][a-zA-Z0-9_]*'}",  # Corresponde ao comando PRINT com espaços no início
}

# Lista de Tokens
tokens = [
            ("tk_bloco_inicio", "ER_BLOCO_INICIO"),          # Corresponde ao início de um bloco
            ("tk_bloco_fim", "ER_BLOCO_FIM"),                # Corresponde ao fim de um bloco
            ("tk_tipo_numero", "ER_TIPO_NUMERO"),            # Corresponde ao tipo NUMERO
            ("tk_tipo_cadeia", "ER_TIPO_CADEIA"),            # Corresponde ao tipo CADEIA
            ("tk_identificador", "ER_IDENTIFICADOR"),        # Corresponde a identificadores de variáveis
            ("tk_numero", "ER_NUMERO"),                      # Corresponde a números inteiros ou reais
            ("tk_cadeia", "ER_CADEIA"),                      # Corresponde a cadeias de caracteres entre aspas duplas
            ("tk_declaracao_numero", "ER_DECLARACAO_NUMERO"),# Declaração de variáveis NUMERO sem inicialização
            ("tk_declaracao_numero_inicializada", "ER_DECLARACAO_NUMERO_INICIALIZADA"),  # Declaração de variáveis NUMERO com inicialização
            ("tk_declaracao_cadeia", "ER_DECLARACAO_CADEIA"),# Declaração de variáveis CADEIA sem inicialização
            ("tk_declaracao_cadeia_inicializada", "ER_DECLARACAO_CADEIA_INICIALIZADA"),  # Declaração de variáveis CADEIA com inicialização
            ("tk_atribuicao_numero", "ER_ATRIBUICAO_NUMERO"),# Atribuição de um número a uma variável
            ("tk_atribuicao_cadeia", "ER_ATRIBUICAO_CADEIA"),# Atribuição de uma cadeia a uma variável
            ("tk_atribuicao_variavel", "ER_ATRIBUICAO_VARIAVEL"),# Atribuição de uma variável a outra variável
            ("tk_print", "ER_PRINT")                         # Corresponde ao comando PRINT
]

#Lista de tokens de declaração
tokens_declaracao = [
            "tk_declaracao_numero",
            "tk_declaracao_numero_inicializada",
            "tk_declaracao_cadeia",
            "tk_declaracao_cadeia_inicializada"
]

#Lista de tokens de atribuição
tokens_atribuicao = [
            "tk_atribuicao_numero",
            "tk_atribuicao_cadeia",
            "tk_atribuicao_variavel",
]

def converte_token_valor_para_tipo(valor, pilha):
    # Lista de expressões regulares ordenadas pela prioridade de verificação
    ordem_prioridade = [
        "ER_DECLARACAO_NUMERO_INICIALIZADA",
        "ER_DECLARACAO_CADEIA_INICIALIZADA",
        "ER_DECLARACAO_NUMERO",
        "ER_DECLARACAO_CADEIA",
        "ER_ATRIBUICAO_NUMERO",
        "ER_ATRIBUICAO_CADEIA",
        "ER_ATRIBUICAO_VARIAVEL",
        "ER_PRINT",
        "ER_BLOCO_INICIO",
        "ER_BLOCO_FIM",
        "ER_TIPO_NUMERO",
        "ER_TIPO_CADEIA",
        "ER_IDENTIFICADOR",
        "ER_NUMERO",
        "ER_CADEIA"
    ]

    # Verificar cada expressão regular na ordem de prioridade
    for nome_ER in ordem_prioridade:
        padrao_ER = ER_DICIONARIO[nome_ER]
        if re.match(padrao_ER, valor):
            for token in tokens:
                if token[1] == nome_ER:
                    if nome_ER == "ER_NUMERO":
                        return tokens[2][0]
                    elif nome_ER == "ER_CADEIA":
                        return tokens[3][0]
                    elif nome_ER == "ER_IDENTIFICADOR":
                        tipo = extrair_tipo_variavel(valor, pilha)
                        if tipo == "NUMERO":
                            return tokens[2][0]
                        elif tipo == "CADEIA":
                            return tokens[3][0]
                    return token[0]
    return -1

def verifica_token_linha(linha):
    # Lista de expressões regulares ordenadas pela prioridade de verificação
    ordem_prioridade = [
        "ER_DECLARACAO_NUMERO_INICIALIZADA",
        "ER_DECLARACAO_CADEIA_INICIALIZADA",
        "ER_DECLARACAO_NUMERO",
        "ER_DECLARACAO_CADEIA",
        "ER_ATRIBUICAO_NUMERO",
        "ER_ATRIBUICAO_CADEIA",
        "ER_ATRIBUICAO_VARIAVEL",
        "ER_PRINT",
        "ER_BLOCO_INICIO",
        "ER_BLOCO_FIM",
        "ER_TIPO_NUMERO",
        "ER_TIPO_CADEIA",
        "ER_IDENTIFICADOR",
        "ER_NUMERO",
        "ER_CADEIA"
    ]

    # Verificar cada expressão regular na ordem de prioridade
    for nome_ER in ordem_prioridade:  # Itera sobre a lista de prioridade de expressões regulares
        padrao_ER = ER_DICIONARIO[nome_ER]  # Obtém o padrão de expressão regular do dicionário
        if re.match(padrao_ER, linha):  # Verifica se a linha corresponde ao padrão atual
            for token in tokens:  # Itera sobre a lista de tokens
                if token[1] == nome_ER:  # Verifica se o token corresponde à expressão regular
                    return token[0]  # Retorna o token correspondente
    return -1  # Retorna -1 se nenhum token corresponder

def extrair_tipo_variavel_declaracao(linha):
    tipo_variavel = linha.split()[0]  # Pega a primeira palavra da linha
    if tipo_variavel in ["NUMERO", "CADEIA"]:  # Verifica se é um tipo válido
        return tipo_variavel  # Retorna o tipo da variável
    return -1  # Retorna -1 se não for um tipo válido

def extrair_tipo_variavel(variavel, pilha):
    for tabela in reversed(pilha):  # Itera sobre a pilha de escopos em ordem reversa
        for simbolo in tabela:  # Itera sobre cada tabela de símbolos
            if simbolo[1] == variavel:  # Verifica se o identificador corresponde à variável
                return simbolo[2]  # Retorna o tipo da variável
    return False  # Retorna False se a variável não for encontrada

def extrair_valor_variavel_atribuicao(linha):
    valor = linha.split('=')[1].strip()  # Separa a linha na posição do '=' e pega a parte direita
    return valor  # Retorna o valor extraído

def extrair_variaveis_tipos_valores_declaracao(linha):
    tipo_variavel = extrair_tipo_variavel_declaracao(linha)  # Extrai o tipo da variável
    if tipo_variavel == -1:  # Verifica se o tipo da variável é inválido
        return -1
    
    variaveis_tipos_valores = []  # Inicializa a lista para armazenar variáveis, tipos e valores
    
    tipo_declaracao = linha.split()[0] 

    linha_sem_tipo = linha[len(tipo_variavel):].strip()  # Remove o tipo da linha

    partes = linha_sem_tipo.split(',')  # Divide a linha em partes separadas por vírgula

    for parte in partes:  # Itera sobre cada parte
        parte = parte.strip()
        if '=' in parte:  # Verifica se há uma atribuição
            variavel, valor = map(str.strip, parte.split('='))  # Separa a variável e o valor
        else:
            variavel = parte
            valor = None  # Valor não inicializado
        token = verifica_token_linha(tipo_declaracao)  # Verifica o token do tipo
        variaveis_tipos_valores.append([token, variavel, tipo_variavel, valor])  # Adiciona à lista
    
    return variaveis_tipos_valores  # Retorna a lista de variáveis, tipos e valores

def extrair_variaveis_print(linha):
    if linha.startswith("PRINT"):  # Verifica se a linha começa com "PRINT"
        partes = linha[5:].strip().split(',')  # Remove "PRINT" e divide pelo separador de vírgula
        variaveis = [parte.strip() for parte in partes]  # Remove espaços em branco de cada parte
        return variaveis  # Retorna a lista de variáveis
    return None  # Retorna None se a linha não começar com "PRINT"

def obter_valor_variavel(variavel, pilha):
    for tabela in reversed(pilha):  # Itera sobre a pilha de escopos em ordem reversa
        for linha in tabela:  # Itera sobre cada linha na tabela de símbolos
            for simbolo in linha:  # Itera sobre cada símbolo na linha
                if simbolo == variavel:  # Verifica se o símbolo corresponde à variável
                    return linha[3]  # Retorna o valor da variável
    return -1  # Retorna -1 se a variável não for encontrada

def obter_tipo_variavel(variavel, pilha):
    for tabela in reversed(pilha):  # Itera sobre a pilha de escopos em ordem reversa
        for linha in tabela:  # Itera sobre cada linha na tabela de símbolos
            for simbolo in linha:  # Itera sobre cada símbolo na linha
                if simbolo == variavel:  # Verifica se o símbolo corresponde à variável
                    return linha[2]  # Retorna o tipo da variável
    return -1  # Retorna -1 se a variável não for encontrada

def verificar_declaracao_variavel(linha, pilha):
    nome_variavel = linha.split('=')[0].strip()  # Separa o nome da variável
    for tabela in reversed(pilha):  # Itera sobre a pilha de escopos em ordem reversa
        for simbolo in tabela:  # Itera sobre cada símbolo na tabela
            if simbolo[1] == nome_variavel:  # Verifica se o identificador corresponde à variável
                return simbolo  # Retorna o símbolo correspondente
    return False  # Retorna False se a variável não for encontrada

def verificar_declaracao_no_escopo_atual(variavel, pilha):
    if not pilha:  # Verifica se a pilha está vazia
        return False
    
    escopo_atual = pilha[-1]  # Obtém o escopo atual (topo da pilha)
    for simbolo in escopo_atual:  # Itera sobre cada símbolo no escopo atual
        if simbolo[1] == variavel:  # Verifica se o identificador corresponde à variável
            return simbolo  # Retorna o símbolo correspondente
    
    return False  # Retorna False se a variável não for encontrada

def atribuir_valor_variavel(linha, pilha, token):
    if token != 'tk_atribuicao_variavel':
        nome_variavel, novo_valor = map(str.strip, linha.split('='))  # Separa a variável e o novo valor
        for tabela in reversed(pilha):  # Itera sobre a pilha de escopos em ordem reversa
            for indice, simbolo in enumerate(tabela):  # Itera sobre cada símbolo na tabela
                if simbolo[1] == nome_variavel:  # Verifica se o identificador corresponde à variável
                    tabela[indice][3] = novo_valor  # Atualiza o valor da variável
                    return True
    else:
        nome_variavel, novo_valor = map(str.strip, linha.split('='))  # Separa a variável e o novo valor
        novo_valor = obter_valor_variavel(novo_valor, pilha)  # Obtém o valor da variável
        tipo_novo_valor = obter_tipo_variavel(novo_valor, pilha)  # Obtém o tipo da variável
        
        for tabela in reversed(pilha):  # Itera sobre a pilha de escopos em ordem reversa
            for indice, simbolo in enumerate(tabela):  # Itera sobre cada símbolo na tabela
                if simbolo[1] == nome_variavel:  # Verifica se o identificador corresponde à variável
                    if simbolo[2] == tipo_novo_valor:  # Verifica se o tipo é compatível
                        tabela[indice][3] = novo_valor  # Atualiza o valor da variável
                        return True
                    else:
                        return -1
        
    return False  # Retorna False se a atribuição falhar

def remover_todos_espacos(linha):
    return re.sub(r'\s+', '', linha)  # Remove todos os espaços da linha

def imprimir_em_arquivo(cadeia, arquivo_saida, index_linha):
    with open(arquivo_saida, "a") as arquivo:  # Abre o arquivo em modo de adição
        arquivo.write( f"[{index_linha + 1}] " + str(cadeia) + "\n")  # Escreve a cadeia no arquivo com o índice da linha
        
def limpar_arquivo_saida(arquivo_saida):
    with open(arquivo_saida, 'w') as arquivo:  # Abre o arquivo em modo de escrita
        arquivo.write("")  # Limpa o conteúdo do arquivo

def main():
    nome_arquivo = "escopo1.txt"  # Nome do arquivo a ser lido
    arquivo_saida = "saida.txt"  # Nome do arquivo de saída
    index_linha = -1  # Inicializa o índice da linha
    pilha = []  # Inicializa a pilha de escopos
    tabela_simbolos = []  # Inicializa a tabela de símbolos

    limpar_arquivo_saida(arquivo_saida)  # Limpa o conteúdo do arquivo de saída

    with open(nome_arquivo, 'r') as arquivo:  # Abre o arquivo de entrada em modo de leitura
        for linha in arquivo:  # Itera sobre cada linha do arquivo
            linha = linha.lstrip()  # Remove espaços em branco no início da linha
            index_linha += 1  # Incrementa o índice da linha

            token_gerado = verifica_token_linha(linha)  # Verifica qual token corresponde à linha

            if token_gerado == -1:  # Se o token gerado for -1 (linha vazia ou inválida)
                print(f"\n[{index_linha + 1}] Linha vazia: {linha}")  # Imprime a linha vazia
            else:
                print(f"\n[{index_linha + 1}] {token_gerado}: {linha}")  # Imprime o token gerado e a linha correspondente

            if token_gerado != -1:  # Se o token gerado não for -1 (linha válida)
                if token_gerado == "tk_bloco_inicio":  # Se o token gerado for o início de um bloco
                    tabela_simbolos = []  # Inicializa uma nova tabela de símbolos
                    pilha.append(tabela_simbolos)  # Adiciona a nova tabela de símbolos à pilha
                if token_gerado == "tk_bloco_fim":  # Se o token gerado for o fim de um bloco
                    pilha.pop()  # Remove a tabela de símbolos do topo da pilha
                if token_gerado in tokens_declaracao:  # Se o token gerado for uma declaração de variável
                    if len(pilha) < 1:  # Se a pilha estiver vazia (declaração fora de um bloco)
                        imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", declaracao de variavel fora de bloco", arquivo_saida, index_linha)  # Imprime um erro no arquivo de saída
                    else:
                        escopos_variaveis = extrair_variaveis_tipos_valores_declaracao(linha)  # Extrai as variáveis, tipos e valores da linha de declaração
                        if escopos_variaveis != -1:  # Se a extração foi bem-sucedida
                            for escopo in escopos_variaveis:  # Itera sobre cada variável, tipo e valor extraído
                                variavel_declarada_escopo_atual = verificar_declaracao_no_escopo_atual(escopo[1], pilha)  # Verifica se a variável já foi declarada no escopo atual
                                if variavel_declarada_escopo_atual == False:  # Se a variável não foi declarada no escopo atual
                                    valor = escopo[3]  # Obtém o valor da variável
                                    if valor != None:  # Se a variável tem um valor inicializado
                                        if (verifica_token_linha(escopo[2]) == converte_token_valor_para_tipo(valor, pilha)):  # Verifica se os tipos são compatíveis
                                            tabela_simbolos.append(escopo)  # Adiciona a variável, tipo e valor à tabela de símbolos
                                        else:
                                            imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", tipos nao compativeis", arquivo_saida, index_linha)  # Imprime um erro no arquivo de saída
                                    else:
                                        tabela_simbolos.append(escopo)  # Adiciona a variável sem valor à tabela de símbolos
                                else:
                                    if len(variavel_declarada_escopo_atual) > 4:  # Verifica se a declaração veio de uma atribuição
                                        variavel_declarada_escopo_atual.pop()  # Remove o último elemento (flag de cópia)
                                        valor = escopo[3]  # Obtém o valor da variável
                                        linha_modificada = f"{variavel_declarada_escopo_atual[1]} = {valor}"  # Cria uma nova linha de atribuição
                                        retorno_atribuicao = atribuir_valor_variavel(linha_modificada, pilha, token_gerado)  # Atribui o novo valor à variável
                                        if retorno_atribuicao == -1:  # Se os tipos não forem compatíveis
                                            imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", tipos nao compativeis", arquivo_saida, index_linha)  # Imprime um erro no arquivo de saída
                                    else:
                                        imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", variavel ja declarada no bloco", arquivo_saida, index_linha)  # Imprime um erro no arquivo de saída

                elif token_gerado in tokens_atribuicao:  # Se o token gerado for uma atribuição de variável
                    if len(pilha) < 1:  # Se a pilha estiver vazia (atribuição fora de um bloco)
                        imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", atribuicao de variavel fora de bloco", arquivo_saida, index_linha)  # Imprime um erro no arquivo de saída
                    else:
                        variavel = verificar_declaracao_variavel(linha, pilha)  # Verifica se a variável foi declarada
                        novo_valor_variavel = extrair_valor_variavel_atribuicao(linha)  # Extrai o novo valor da variável
                        if variavel != False:  # Se a variável foi encontrada
                            if verificar_declaracao_no_escopo_atual(variavel[1], pilha) != False:  # Se a variável foi declarada no escopo atual
                                if verifica_token_linha(variavel[2]) == converte_token_valor_para_tipo(novo_valor_variavel, pilha):  # Verifica se os tipos são compatíveis
                                    retorno_atribuicao = atribuir_valor_variavel(linha, pilha, token_gerado)  # Atribui o novo valor à variável
                                    if retorno_atribuicao == -1:  # Se os tipos não forem compatíveis
                                        imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", tipos nao compativeis", arquivo_saida, index_linha)  # Imprime um erro no arquivo de saída
                                else:
                                    imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", tipos nao compativeis", arquivo_saida, index_linha)  # Imprime um erro no arquivo de saída
                            else:
                                if variavel[3] != None:  # Se a variável tem um valor inicializado
                                    if verifica_token_linha(variavel[3]) == verifica_token_linha(novo_valor_variavel):  # Verifica se os tipos são compatíveis
                                        variavel_aux = copy.deepcopy(variavel)  # Cria uma cópia da variável
                                        variavel_aux[3] = novo_valor_variavel  # Atualiza o valor da cópia
                                        variavel_aux.append("copia-atribuicao")  # Adiciona uma flag de cópia
                                        tabela_simbolos.append(variavel_aux)  # Adiciona a cópia à tabela de símbolos
                                    else:
                                        imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", tipos nao compativeis", arquivo_saida, index_linha)  # Imprime um erro no arquivo de saída
                                else:
                                    variavel_aux = copy.deepcopy(variavel)  # Cria uma cópia da variável
                                    variavel_aux[3] = novo_valor_variavel  # Atualiza o valor da cópia
                                    variavel_aux.append("copia-atribuicao")  # Adiciona uma flag de cópia
                                    tabela_simbolos.append(variavel_aux)  # Adiciona a cópia à tabela de símbolos
                        else:
                            imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", variavel nao declarada", arquivo_saida, index_linha)  # Imprime um erro no arquivo de saída
                elif token_gerado == "tk_print":  # Se o token gerado for um comando PRINT
                    if len(pilha) < 1:  # Se a pilha estiver vazia (PRINT fora de um bloco)
                        imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", print fora de bloco", arquivo_saida, index_linha)  # Imprime um erro no arquivo de saída
                    else:
                        variaveis_print = extrair_variaveis_print(linha)  # Extrai as variáveis do comando PRINT
                        for variavel in variaveis_print:  # Itera sobre cada variável a ser impressa
                            valor_variavel = obter_valor_variavel(variavel, pilha)  # Obtém o valor da variável
                            if valor_variavel != -1:  # Se a variável foi encontrada
                                imprimir_em_arquivo(valor_variavel, arquivo_saida, index_linha)  # Imprime o valor da variável no arquivo de saída
                            else:
                                imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", variavel nao declarada", arquivo_saida, index_linha)  # Imprime um erro no arquivo de saída
                elif token_gerado == "tk_tipo_numero" or token_gerado == "tk_tipo_cadeia":  # Se o token gerado for um tipo NUMERO ou CADEIA
                    imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", comando mal utilizado", arquivo_saida, index_linha)  # Imprime um erro no arquivo de saída
                elif token_gerado == "tk_numero":  # Se o token gerado for um número
                    imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", numero sem atribuicao", arquivo_saida, index_linha)  # Imprime um erro no arquivo de saída
                elif token_gerado == "tk_cadeia":  # Se o token gerado for uma cadeia
                    imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", cadeia sem atribuicao", arquivo_saida, index_linha)  # Imprime um erro no arquivo de saída
                elif token_gerado == "tk_identificador":  # Se o token gerado for um identificador
                    imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", variavel sem atribuicao", arquivo_saida, index_linha)  # Imprime um erro no arquivo de saída

            print(f"      PILHA: {pilha}")  # Imprime o estado atual da pilha

main()  # Chama a função principal para executar o programa