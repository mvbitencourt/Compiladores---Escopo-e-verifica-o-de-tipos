import re

# Dicionário de Expressões Regulares
ER_DICIONARIO = {
    "ER_BLOCO_INICIO": r"BLOCO \w+",  # Corresponde ao início de um bloco com qualquer palavra
    "ER_BLOCO_FIM": r"FIM \w+",       # Corresponde ao fim de um bloco com qualquer palavra
    "ER_TIPO_NUMERO": r"NUMERO",
    "ER_TIPO_CADEIA": r"CADEIA",
    "ER_IDENTIFICADOR": r"[a-zA-Z_][a-zA-Z0-9_]*",
    "ER_NUMERO": r"[+-]?\d+(\.\d+)?",
    "ER_CADEIA": r'"([^"]*)"',
    "ER_DECLARACAO_NUMERO": fr"NUMERO\s+{r'[a-zA-Z_][a-zA-Z0-9_]*'}(,\s*{r'[a-zA-Z_][a-zA-Z0-9_]*'})*",
    "ER_DECLARACAO_NUMERO_INICIALIZADA": fr"NUMERO\s+({r'[a-zA-Z_][a-zA-Z0-9_]*'}\s*=\s*{r'[+-]?\d+(\.\d+)?'}\s*,\s*)*{r'[a-zA-Z_][a-zA-Z0-9_]*'}\s*=\s*{r'[+-]?\d+(\.\d+)?'}",
    "ER_DECLARACAO_CADEIA": fr"CADEIA\s+{r'[a-zA-Z_][a-zA-Z0-9_]*'}(,\s*{r'[a-zA-Z_][a-zA-Z0-9_]*'})*",
    "ER_DECLARACAO_CADEIA_INICIALIZADA": fr"CADEIA\s+({r'[a-zA-Z_][a-zA-Z0-9_]*'}\s*=\s*{r'\"([^"]*)\"'}\s*,\s*)*{r'[a-zA-Z_][a-zA-Z0-9_]*'}\s*=\s*{r'\"([^"]*)\"'}",
    "ER_ATRIBUICAO_NUMERO": fr"{r'[a-zA-Z_][a-zA-Z0-9_]*'}\s*=\s*{r'[+-]?\d+(\.\d+)?'}",
    "ER_ATRIBUICAO_CADEIA": fr"{r'[a-zA-Z_][a-zA-Z0-9_]*'}\s*=\s*{r'\"([^"]*)\"'}",
    "ER_ATRIBUICAO_VARIAVEL": fr"{r'[a-zA-Z_][a-zA-Z0-9_]*'}\s*=\s*{r'[a-zA-Z_][a-zA-Z0-9_]*'}",
    "ER_PRINT": fr"PRINT\s+{r'[a-zA-Z_][a-zA-Z0-9_]*'}"
}

# Lista de Tokens
tokens = [
    ("tk_bloco_inicio", "ER_BLOCO_INICIO"),          
    ("tk_bloco_fim", "ER_BLOCO_FIM"),                
    ("tk_tipo_numero", "ER_TIPO_NUMERO"),            
    ("tk_tipo_cadeia", "ER_TIPO_CADEIA"),            
    ("tk_identificador", "ER_IDENTIFICADOR"),        
    ("tk_numero", "ER_NUMERO"),                      
    ("tk_cadeia", "ER_CADEIA"),                      
    ("tk_declaracao_numero", "ER_DECLARACAO_NUMERO"),
    ("tk_declaracao_numero_inicializada", "ER_DECLARACAO_NUMERO_INICIALIZADA"),
    ("tk_declaracao_cadeia", "ER_DECLARACAO_CADEIA"),
    ("tk_declaracao_cadeia_inicializada", "ER_DECLARACAO_CADEIA_INICIALIZADA"),
    ("tk_atribuicao_numero", "ER_ATRIBUICAO_NUMERO"),
    ("tk_atribuicao_cadeia", "ER_ATRIBUICAO_CADEIA"),
    ("tk_atribuicao_variavel", "ER_ATRIBUICAO_VARIAVEL"),
    ("tk_print", "ER_PRINT")
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

    for nome_ER in ordem_prioridade:
        padrao_ER = ER_DICIONARIO[nome_ER]
        if re.match(padrao_ER, linha):
            for token in tokens:
                if token[1] == nome_ER:
                    return token[0]
    return -1

def extrair_tipo_variavel(linha):
    tipo_variavel = linha.split()[0]
    print(tipo_variavel)
    if tipo_variavel in ["NUMERO", "CADEIA"]:
        return tipo_variavel
    return -1

def extrair_variaveis_tipos_valores(linha):
    tipo_variavel = extrair_tipo_variavel(linha)
    variaveis_tipos_valores = []

    linha_sem_tipo = linha[len(tipo_variavel):].strip()
    partes = linha_sem_tipo.split(',')

    for parte in partes:
        parte = parte.strip()
        if '=' in parte:
            variavel, valor = map(str.strip, parte.split('='))
        else:
            variavel = parte
            valor = None
        variaveis_tipos_valores.append((variavel, tipo_variavel, valor))

    return variaveis_tipos_valores

def extrair_variaveis_print(linha):
    if linha.startswith("PRINT"):
        partes = linha[5:].strip().split(',')
        variaveis = [parte.strip() for parte in partes]
        return variaveis
    return None

def obter_valor_variavel(variavel, pilha):
    for escopo in reversed(pilha):
        if variavel in escopo:
            return escopo[variavel]['valor']
    return None

def declarar_variavel(tabela_simbolos, nome_variavel, tipo_variavel, valor_inicial=None):
    if nome_variavel in tabela_simbolos:
        raise ValueError(f"Erro: Variável '{nome_variavel}' já declarada neste escopo.")
    
    tabela_simbolos[nome_variavel] = {
        'tipo': tipo_variavel,
        'valor': valor_inicial
    }

def atualizar_pilha(pilha, tabela_simbolos):
    if pilha:
        pilha[-1] = tabela_simbolos

def atualiza_tabela_simbolos(linha, tabela_simbolos):
    variaveis_tipos_valores = extrair_variaveis_tipos_valores(linha)
    for variavel, tipo_variavel, valor in variaveis_tipos_valores:
        encontrado = False
        for simbolo in tabela_simbolos:
            if simbolo == variavel:
                if tabela_simbolos[simbolo]['tipo'] == tipo_variavel:
                    tabela_simbolos[simbolo]['valor'] = valor
                else:
                    return -2
                encontrado = True
        if not encontrado:
            return -1
        elif encontrado:
            return tabela_simbolos

def imprimir_em_arquivo(cadeia, arquivo_saida):
    with open(arquivo_saida, "a") as arquivo:
        arquivo.write(str(cadeia) + "\n")

def limpar_arquivo_saida(arquivo_saida):
    with open(arquivo_saida, 'w') as arquivo:
        arquivo.write("")

def main():
    nome_arquivo = "escopo.txt"
    arquivo_saida = "saida.txt"
    linhas = []
    index_linha = -1
    erro = ""
    pilha = []
    tabela_simbolos = []
    lista_print = []

    limpar_arquivo_saida(arquivo_saida)

    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            index_linha += 1

            token_gerado = verifica_token(linha)
            
            print(f"[{index_linha}] {token_gerado}: {linha}")
            
            if token_gerado != -1:
                if token_gerado == "tk_bloco_inicio":
                    tabela_simbolos = {}
                    pilha.append(tabela_simbolos)
                elif token_gerado == "tk_bloco_fim":
                    if pilha:
                        tabela_simbolos = pilha.pop()
                elif token_gerado in tokens_declaracao:
                    variaveis_tipos_valores = extrair_variaveis_tipos_valores(linha)
                    for variavel, tipo_variavel, valor in variaveis_tipos_valores:
                        try:
                            declarar_variavel(tabela_simbolos, variavel, tipo_variavel, valor)
                        except ValueError as e:
                            erro = str(e)
                    atualizar_pilha(pilha, tabela_simbolos)
                elif token_gerado in tokens_atribuicao:
                    tabela_nova = atualiza_tabela_simbolos(linha, tabela_simbolos)
                    if tabela_nova != -1 and tabela_nova != -2:
                        tabela_simbolos = tabela_nova
                    atualizar_pilha(pilha, tabela_simbolos)
                elif token_gerado == "tk_print":
                    variaveis_print = extrair_variaveis_print(linha)
                    for variavel in variaveis_print:
                        valor_variavel = obter_valor_variavel(variavel, pilha)
                        if valor_variavel is not None:
                            imprimir_em_arquivo(valor_variavel, arquivo_saida)
                        else:
                            erro = f"Erro linha {index_linha + 1} - Variável '{variavel}' não declarada"
                            imprimir_em_arquivo(erro, arquivo_saida)
                    
            linhas.append([index_linha, linha, erro])

main()