import re
import copy

comandos = ["BLOCO", "FIM", "NUMERO", "CADEIA", "PRINT"]

# Dicionário de Expressões Regulares
ER_DICIONARIO = {
    "ER_BLOCO_INICIO": r"\s*BLOCO \w+",  # Corresponde ao início de um bloco com qualquer palavra e espaços no início
    "ER_BLOCO_FIM": r"\s*FIM \w+",       # Corresponde ao fim de um bloco com qualquer palavra e espaços no início
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

tokens_declaracao = [
            "tk_declaracao_numero",
            "tk_declaracao_numero_inicializada",
            "tk_declaracao_cadeia",
            "tk_declaracao_cadeia_inicializada"
]

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
    for nome_ER in ordem_prioridade:
        padrao_ER = ER_DICIONARIO[nome_ER]
        if re.match(padrao_ER, linha):
            for token in tokens:
                if token[1] == nome_ER:
                    return token[0]
    return -1

def extrair_tipo_variavel_declaracao(linha):
    tipo_variavel = linha.split()[0]  # Pega a primeira palavra da linha
    if tipo_variavel in ["NUMERO", "CADEIA"]:
        return tipo_variavel
    return -1

def extrair_tipo_variavel(variavel, pilha):
    
    for tabela in reversed(pilha):
        for simbolo in tabela:
            if simbolo[1] == variavel:
                return simbolo[2]
    return False

# EXCLUIR
def extrair_variavel_atribuicao(linha):
    variavel = linha.split()[0]  # Pega a primeira palavra da linha
    padrao_ER = ER_DICIONARIO["ER_IDENTIFICADOR"]

    if re.match(padrao_ER, variavel):
        return variavel
    return -1

def extrair_valor_variavel_atribuicao(linha):
    # Separar a linha na posição do '=' e pegar a parte direita
    valor = linha.split('=')[1].strip()
    return valor

def extrair_variaveis_tipos_valores_declaracao(linha):
    tipo_variavel = extrair_tipo_variavel_declaracao(linha)
    if tipo_variavel == -1:
        return -1
    
    variaveis_tipos_valores = []

    # Remover o tipo da linha
    linha_sem_tipo = linha[len(tipo_variavel):].strip()

    # Dividir a linha em partes separadas por vírgula
    partes = linha_sem_tipo.split(',')

    for parte in partes:
        parte = parte.strip()
        if '=' in parte:
            variavel, valor = map(str.strip, parte.split('='))
        else:
            variavel = parte
            valor = None  # Valor não inicializado
        token = verifica_token_linha(variavel)
        variaveis_tipos_valores.append([token, variavel, tipo_variavel, valor])
    
    return variaveis_tipos_valores

def extrair_variaveis_print(linha):
    if linha.startswith("PRINT"):
        partes = linha[5:].strip().split(',')  # Remove "PRINT", remove espaços em branco e divide pelo separador de vírgula
        variaveis = [parte.strip() for parte in partes]
        return variaveis
    return None

def obter_valor_variavel(variavel, pilha):
    for tabela in reversed(pilha):
        for linha in tabela:
            for simbolo in linha:
                if simbolo == variavel:
                    return linha[3]
    return -1

def obter_tipo_variavel(variavel, pilha):
    for tabela in reversed(pilha):
        for linha in tabela:
            for simbolo in linha:
                if simbolo == variavel:
                    return linha[2]
    return -1

def verificar_declaracao_variavel(linha, pilha):
    # Separar o nome da variável
    nome_variavel = linha.split('=')[0].strip()
    
    # Procurar na pilha se a variável foi declarada
    for tabela in reversed(pilha):
        for simbolo in tabela:
            if simbolo[1] == nome_variavel:
                return simbolo
    return False

def verificar_declaracao_no_escopo_atual(variavel, pilha):
    if not pilha:
        return False
    
    escopo_atual = pilha[-1]
    for simbolo in escopo_atual:
        if simbolo[1] == variavel:
            return simbolo
    
    return False

def atribuir_valor_variavel(linha, pilha, token):
    if token != 'tk_atribuicao_variavel':
        # Separar a variável e o novo valor
        nome_variavel, novo_valor = map(str.strip, linha.split('='))
        #nome_variavel = remover_todos_espacos(nome_variavel)
        #novo_valor = remover_todos_espacos(novo_valor)
        
        # Procurar na pilha a variável e atualizar seu valor
        for tabela in reversed(pilha):
            for indice, simbolo in enumerate(tabela):
                if simbolo[1] == nome_variavel:
                    tabela[indice][3] = novo_valor
                    return True

    else:
        # Separar a variável e o novo valor
        nome_variavel, novo_valor = map(str.strip, linha.split('='))
        novo_valor = obter_valor_variavel(novo_valor, pilha)
        tipo_novo_valor = obter_tipo_variavel(novo_valor, pilha)
        
        # Procurar na pilha a variável e atualizar seu valor
        for tabela in reversed(pilha):
            for indice, simbolo in enumerate(tabela):
                if simbolo[1] == nome_variavel:
                    if simbolo[2] == tipo_novo_valor:
                        tabela[indice][3] = novo_valor
                        return True
                    else:
                        return -1

        
    return False

def atualiza_tabela_declaracao(tabela_simbolos, nome_variavel, tipo_variavel, valor_inicial):
    if nome_variavel in tabela_simbolos:
        raise ValueError(f"Erro: Variável '{nome_variavel}' já declarada neste escopo.")
    
    tabela_simbolos[nome_variavel] = {
        'tipo': tipo_variavel,
        'valor': valor_inicial
    }
        
def atualizar_pilha(pilha, tabela_simbolos):
    if pilha:
        pilha[-1] = tabela_simbolos  # Atualiza a pilha com a versão mais recente da tabela
    return pilha

def remover_todos_espacos(linha):
    return re.sub(r'\s+', '', linha)

def imprimir_em_arquivo(cadeia, arquivo_saida, index_linha):
    with open(arquivo_saida, "a") as arquivo:
        arquivo.write( f"[{index_linha + 1}] " + str(cadeia) + "\n")
        
def limpar_arquivo_saida(arquivo_saida):
    with open(arquivo_saida, 'w') as arquivo:
        arquivo.write("")

def main():
    nome_arquivo = "escopo3.txt" # Nome do arquivo a ser lido
    arquivo_saida = "saida.txt"
    index_linha = -1
    pilha = []
    tabela_simbolos = []

    limpar_arquivo_saida(arquivo_saida)

    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            linha = linha.lstrip()
            index_linha += 1

            token_gerado = verifica_token_linha(linha)
            
            print(f"\n[{index_linha + 1}] {token_gerado}: {linha}")
            print(token_gerado)
            
            if token_gerado != -1:
                if token_gerado  == "tk_bloco_inicio":
                    tabela_simbolos = []
                    pilha.append(tabela_simbolos)
                if token_gerado  == "tk_bloco_fim":
                    pilha.pop()
                if token_gerado in tokens_declaracao:
                    if len(pilha) < 1:
                        imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", declaracao de variavel fora de bloco", arquivo_saida, index_linha)
                    else: 
                        escopos_variaveis = extrair_variaveis_tipos_valores_declaracao(linha)
                        if escopos_variaveis != -1:
                            for escopo in escopos_variaveis:
                                variavel_declarada_escopo_atual = verificar_declaracao_no_escopo_atual(escopo[1], pilha)
                                if variavel_declarada_escopo_atual == False:
                                    valor = escopo[3]
                                    if valor != None:
                                        if (verifica_token_linha(escopo[2]) == converte_token_valor_para_tipo(valor, pilha)):
                                            tabela_simbolos.append(escopo)
                                        else:
                                            imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", tipos nao compativeis", arquivo_saida, index_linha)
                                    else:
                                        tabela_simbolos.append(escopo)
                                else:
                                    if len(variavel_declarada_escopo_atual) > 4: # Verifica se declaração veio de uma atribuição 
                                        variavel_declarada_escopo_atual.pop()
                                        valor = escopo[3]
                                        linha_modificada = f"{variavel_declarada_escopo_atual[1]} = {valor}"
                                        retorno_atribuicao = atribuir_valor_variavel(linha_modificada, pilha, token_gerado)
                                        if retorno_atribuicao == -1:
                                            imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", tipos nao compativeis", arquivo_saida, index_linha)
                                    else:
                                        imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", variavel ja declarada no bloco", arquivo_saida, index_linha)
                                    
                elif token_gerado in tokens_atribuicao:
                    if len(pilha) < 1:
                        imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", atribuicao de variavel fora de bloco", arquivo_saida, index_linha)
                    else:
                        variavel = verificar_declaracao_variavel(linha, pilha)
                        print(variavel)
                        novo_valor_variavel = extrair_valor_variavel_atribuicao(linha)
                        print(novo_valor_variavel)
                        if variavel != False:
                            if verificar_declaracao_no_escopo_atual(variavel[1], pilha) != False:
                                if verifica_token_linha(variavel[2]) == converte_token_valor_para_tipo(novo_valor_variavel, pilha):
                                    retorno_atribuicao = atribuir_valor_variavel(linha, pilha, token_gerado)
                                    if retorno_atribuicao == -1:
                                        imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", tipos nao compativeis", arquivo_saida, index_linha)
                                else:
                                    imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", tipos nao compativeis", arquivo_saida, index_linha)
                            else:
                                if variavel[3] != None:
                                    if verifica_token_linha(variavel[3]) == verifica_token_linha(novo_valor_variavel):
                                        variavel_aux = copy.deepcopy(variavel) 
                                        variavel_aux[3] = novo_valor_variavel
                                        variavel_aux.append("copia-atribuicao")
                                        tabela_simbolos.append(variavel_aux)
                                    else:
                                        imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", tipos nao compativeis", arquivo_saida, index_linha)
                                else:
                                    variavel_aux = copy.deepcopy(variavel) 
                                    variavel_aux[3] = novo_valor_variavel
                                    variavel_aux.append("copia-atribuicao")
                                    tabela_simbolos.append(variavel_aux)
                        else:
                            imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", variavel nao declarada", arquivo_saida, index_linha)
                elif token_gerado == "tk_print":
                    if len(pilha) < 1:
                        imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", print fora de bloco", arquivo_saida, index_linha)
                    else:
                        variaveis_print = extrair_variaveis_print(linha)
                        for variavel in variaveis_print:
                            valor_variavel = obter_valor_variavel(variavel, pilha)
                            if valor_variavel != -1:
                                imprimir_em_arquivo(valor_variavel, arquivo_saida, index_linha)
                            else:
                                imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", variavel nao declarada", arquivo_saida, index_linha)           
                elif token_gerado == "tk_tipo_numero" or token_gerado == "tk_tipo_cadeia":
                    imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", comando mal utilizado", arquivo_saida, index_linha)
                elif token_gerado == "tk_numero":
                    imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", numero sem atibuicao", arquivo_saida, index_linha)
                elif token_gerado == "tk_cadeia":
                    imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", cadeia sem atribuicao", arquivo_saida, index_linha)
                elif token_gerado == "tk_identificador":
                    imprimir_em_arquivo("Erro linha " + str(index_linha + 1) + ", variavel sem atribuicao", arquivo_saida, index_linha)

            print(f"PILHA: {pilha}")

main()