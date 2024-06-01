import re

comandos = ["BLOCO", "FIM", "NUMERO", "CADEIA", "PRINT"]

# Dicionário de Expressões Regulares
ER_DICIONARIO = {
    # Expressões regulares definidas
    "ER_BLOCO_INICIO": r"BLOCO \w+",               # Corresponde ao início de um bloco 
    "ER_BLOCO_FIM": r"FIM \w+",                 # Corresponde ao fim de um bloco 
    "ER_TIPO_NUMERO": r"NUMERO",                   # Corresponde ao tipo NUMERO
    "ER_TIPO_CADEIA": r"CADEIA",                   # Corresponde ao tipo CADEIA
    "ER_IDENTIFICADOR": r"[a-zA-Z_][a-zA-Z0-9_]*", # Corresponde a identificadores de variáveis
    "ER_NUMERO": r"[+-]?\d+(\.\d+)?",              # Corresponde a números inteiros ou reais
    "ER_CADEIA": r'"([^"]*)"',                     # Corresponde a cadeias de caracteres entre aspas duplas

    # Declarações de variáveis tipo NUMERO
    "ER_DECLARACAO_NUMERO": fr"NUMERO\s+{r'[a-zA-Z_][a-zA-Z0-9_]*'}(,\s*{r'[a-zA-Z_][a-zA-Z0-9_]*'})*",  # Declaração de variáveis NUMERO sem inicialização
    "ER_DECLARACAO_NUMERO_INICIALIZADA": fr"NUMERO\s+({r'[a-zA-Z_][a-zA-Z0-9_]*'}\s*=\s*{r'[+-]?\d+(\.\d+)?'}\s*,\s*)*{r'[a-zA-Z_][a-zA-Z0-9_]*'}\s*=\s*{r'[+-]?\d+(\.\d+)?'}",  # Declaração de variáveis NUMERO com inicialização

    # Declarações de variáveis tipo CADEIA
    "ER_DECLARACAO_CADEIA": fr"CADEIA\s+{r'[a-zA-Z_][a-zA-Z0-9_]*'}(,\s*{r'[a-zA-Z_][a-zA-Z0-9_]*'})*",  # Declaração de variáveis CADEIA sem inicialização
    "ER_DECLARACAO_CADEIA_INICIALIZADA": fr"CADEIA\s+({r'[a-zA-Z_][a-zA-Z0-9_]*'}\s*=\s*{r'\"([^"]*)\"'}\s*,\s*)*{r'[a-zA-Z_][a-zA-Z0-9_]*'}\s*=\s*{r'\"([^"]*)\"'}",  # Declaração de variáveis CADEIA com inicialização

    # Atribuições de variáveis
    "ER_ATRIBUICAO_NUMERO": fr"{r'[a-zA-Z_][a-zA-Z0-9_]*'}\s*=\s*{r'[+-]?\d+(\.\d+)?'}",  # Atribuição de um número a uma variável
    "ER_ATRIBUICAO_CADEIA": fr"{r'[a-zA-Z_][a-zA-Z0-9_]*'}\s*=\s*{r'\"([^"]*)\"'}",  # Atribuição de uma cadeia a uma variável
    "ER_ATRIBUICAO_VARIAVEL": fr"{r'[a-zA-Z_][a-zA-Z0-9_]*'}\s*=\s*{r'[a-zA-Z_][a-zA-Z0-9_]*'}",  # Atribuição de uma variável a outra variável

    # Comandos PRINT
    "ER_PRINT": fr"PRINT\s+{r'[a-zA-Z_][a-zA-Z0-9_]*'}"    # Corresponde ao comando PRINT
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

def verifica_token(linha):
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

def extrair_variavel_atribuicao(linha):
    variavel = linha.split()[0]  # Pega a primeira palavra da linha
    padrao_ER = ER_DICIONARIO["ER_IDENTIFICADOR"]

    if re.match(padrao_ER, variavel):
        return variavel
    return -1

def extrair_variaveis_tipos_valores_declaracao(linha):
    tipo_variavel = extrair_tipo_variavel_declaracao(linha)
    if tipo_variavel is -1:
        raise ValueError("Tipo de variável não reconhecido na linha: " + linha)
    
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
        token = verifica_token(variavel)
        variaveis_tipos_valores.append([token, variavel, tipo_variavel, valor])
    
    return variaveis_tipos_valores

def extrair_variaveis_tipos_valores_atribuicao(linha):
    variavel = extrair_variavel_atribuicao(linha)
    if variavel is -1:
        raise ValueError("variável não reconhecido na linha: " + linha)
    
    variaveis_tipos_valores = []

    # Remover o tipo da linha
    linha_sem_tipo = linha[len(variavel):].strip()

    # Dividir a linha em partes separadas por vírgula
    partes = linha_sem_tipo.split(',')

    for parte in partes:
        parte = parte.strip()
        if '=' in parte:
            variavel, valor = map(str.strip, parte.split('='))
        else:
            variavel = parte
            valor = None  # Valor não inicializado
        token = verifica_token(variavel)
        variaveis_tipos_valores.append([token, variavel, variavel, valor])
    
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

def verificar_declaracao_variavel(linha, pilha):
    # Separar o nome da variável
    nome_variavel = linha.split('=')[0].strip()
    
    # Procurar na pilha se a variável foi declarada
    for escopo in reversed(pilha):
        if nome_variavel in escopo:
            return escopo[nome_variavel]
    return False

def atualiza_tabela_simbolos(linha, tabela_simbolos):
    variaveis_tipos_valores = extrair_variaveis_tipos_valores_atribuicao(linha)
    for variavel, tipo_variavel, valor in variaveis_tipos_valores:
        encontrado = False
        for simbolo in tabela_simbolos:
            if simbolo[0] == variavel:
                if simbolo[1] == tipo_variavel:
                    simbolo[2] = valor
                else:
                    return -2
                encontrado = True
        if not encontrado:
            return -1
        elif encontrado:
            return tabela_simbolos     

def atualiza_tabela_declaracao(tabela_simbolos, nome_variavel, tipo_variavel, valor_inicial):
    if nome_variavel in tabela_simbolos:
        raise ValueError(f"Erro: Variável '{nome_variavel}' já declarada neste escopo.")
    
    tabela_simbolos[nome_variavel] = {
        'tipo': tipo_variavel,
        'valor': valor_inicial
    }

def verificar_tipo_erro(linha, comandos):
    for comando in comandos:
        if comando in linha:
            if comandos.index(comando) < 2:
                return f"comando '{comando}' mal utilizado"
            elif 1 < comandos.index(comando) < 4:
                return f"inconsistencia de tipagem"
            else:
                # PROBLEMAS DE DECLARAÇÃO DE VARIAVEL
                return
        else:
            # PROBLEMAS DE ATRIBUIÇÃO
            return
        
def atualizar_pilha(pilha, tabela_simbolos):
    if pilha:
        pilha[-1] = tabela_simbolos  # Atualiza a pilha com a versão mais recente da tabela
    return pilha

def pilha_vazia(pilha):
    if len(pilha) == 0:
        return True
    else:
        return False

def imprimir_em_arquivo(cadeia, arquivo_saida):
    with open(arquivo_saida, "a") as arquivo:
        arquivo.write(str(cadeia) + "\n")
        
def limpar_arquivo_saida(arquivo_saida):
    with open(arquivo_saida, 'w') as arquivo:
        arquivo.write("")

def main():
    nome_arquivo = "escopo.txt" # Nome do arquivo a ser lido
    arquivo_saida = "saida.txt"
    linhas = [] # Inicializa uma lista vazia para armazenar as linhas
    index_linha = -1
    erro = ""
    pilha = []
    tabela_simbolos = []
    bloco_aberto = False

    limpar_arquivo_saida(arquivo_saida)

    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            index_linha += 1

            token_gerado = verifica_token(linha)
            
            print(f"[{index_linha}] {token_gerado}: {linha}")
            
            if token_gerado != -1:
                if token_gerado  == "tk_bloco_inicio":
                    pilha.append(tabela_simbolos)
                if token_gerado  == "tk_bloco_fim":
                    pilha.pop()
                if token_gerado in tokens_declaracao:
                    if pilha_vazia(pilha):
                        imprimir_em_arquivo("Erro linha " + str(index_linha) + ", declaracao de variavel fora de bloco", arquivo_saida)
                    else: 
                        escopos_variaveis = extrair_variaveis_tipos_valores_declaracao(linha)
                        for escopo in escopos_variaveis:
                            tabela_simbolos.append(escopo)
                elif token_gerado in tokens_atribuicao:
                    if pilha_vazia(pilha):
                        imprimir_em_arquivo("Erro linha " + str(index_linha) + ", atribuicao de variavel fora de bloco", arquivo_saida)
                    else:
                        if verificar_declaracao_variavel(linha, pilha) != False:
                            escopo_variavel = verificar_declaracao_variavel(linha, pilha)
                            print(escopo_variavel)
                            tabela_nova = atualiza_tabela_simbolos(linha, tabela_simbolos)
                            if tabela_nova != -1 and tabela_nova != -2:
                                tabela_simbolos = tabela_nova
                        else:
                            imprimir_em_arquivo("Erro linha " + str(index_linha) + ", variavel nao declarada", arquivo_saida)
                elif token_gerado == "tk_print":
                    if pilha_vazia(pilha):
                        imprimir_em_arquivo("Erro linha " + str(index_linha) + ", declaracao de variavel fora de bloco", arquivo_saida)
                    else:
                        variaveis_print = extrair_variaveis_print(linha)
                        for variavel in variaveis_print:
                            valor_variavel = obter_valor_variavel(variavel, pilha)
                            imprimir_em_arquivo(valor_variavel, arquivo_saida)
        
            linhas.append([index_linha, linha, erro])
            print(f"PILHA: {pilha}")

main()