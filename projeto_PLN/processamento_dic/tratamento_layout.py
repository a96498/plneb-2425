import re
import json


#------------------------------------------
#   pre processamento dicionario com -layout --- transformar 2 colunas em 1 coluna

def processar_pdf_duas_colunas(texto):
    paginas = texto.split('\f')
    resultado = []

    for pagina in paginas:
        linhas = pagina.splitlines()
        col_esquerda = []
        col_direita = []

        for linha in linhas:
            if len(linha.strip()) == 0:
                continue
            corte = 60  
            col_esquerda.append(linha[:corte].rstrip())
            col_direita.append(linha[corte:].strip())

        # Junta as duas colunas como se fossem uma única coluna de leitura
        texto_pagina = '\n'.join(col_esquerda + col_direita)
        resultado.append(texto_pagina.strip())

    return '\n\n'.join(resultado)

# Leitura do ficheiro
with open("processamento_dic\diccionari_layout.txt", "r", encoding="utf-8") as f:
    texto_original = f.read()

# Processamento
texto_corrigido = processar_pdf_duas_colunas(texto_original)

# Salvar resultado
with open("processamento_dic\diccionari_layout_alterado.txt", "w", encoding="utf-8") as f:
    f.write(texto_corrigido)




#--------------------------------------------------------------------------------------------------------------------
# limpeza e marcas

def tira_espaco(texto):
    linhas = texto.splitlines()
    linhas_sem_espacos = [linha.lstrip() for linha in linhas]
    return "\n".join(linhas_sem_espacos)

def tira_numpag(texto_dicionario):
    return re.sub(r'\n\d{1,3}$', '', texto_dicionario, flags=re.UNICODE | re.MULTILINE)

def tira_cabecalho(texto):  #às vezes aparece cortado por causa das colunas
    texto = re.sub(r'QUADERNS 50 DICCIONARI MULTILINGÜE DE LA COVID-19', '', texto, flags=re.UNICODE)
    texto = re.sub(r'QUADE\n', '', texto, flags=re.UNICODE)
    texto = re.sub(r'RNS 50 DICCIONARI MULTILINGÜE DE LA COVID-19', '', texto, flags=re.UNICODE)
    texto = re.sub(r'QUAD\n', '', texto, flags=re.UNICODE)
    texto = re.sub(r'ERNS 50 DICCIONARI MULTILINGÜE DE LA COVID-19', '', texto, flags=re.UNICODE)
    texto = re.sub(r'QUA\n', '', texto, flags=re.UNICODE)
    texto = re.sub(r'DERNS 50 DICCIONARI MULTILINGÜE DE LA COVID-19', '', texto, flags=re.UNICODE)
    texto = re.sub(r'QU\n', '', texto, flags=re.UNICODE)
    texto = re.sub(r'ADERNS 50 DICCIONARI MULTILINGÜE DE LA COVID-19', '', texto, flags=re.UNICODE)
    texto = re.sub(r'ADE', '', texto, flags=re.UNICODE)
    texto = re.sub(r'Diccionari', '', texto, flags=re.UNICODE)
    texto = re.sub(r'\u202b', '', texto, flags=re.UNICODE)
    texto = re.sub(r'\u202c', '', texto, flags=re.UNICODE)
    return texto

def tira_letra(texto):
    return re.sub(r'\b[A-Z]\b', '', texto, flags=re.UNICODE)

def limpeza_texto(path_texto):
    with open(path_texto, "r", encoding="utf-8") as f:
        texto = f.read()

    texto_pag = tira_numpag(texto) 
    texto_cab = tira_cabecalho(texto_pag)
    texto_limpo = tira_letra(texto_cab)
    texto_alinhado = tira_espaco(texto_limpo)

    with open(path_texto, "w", encoding="utf-8") as f:
        f.write(texto_alinhado)


limpeza_texto(r'processamento_dic/diccionari_layout_alterado.txt')





def marca_def(texto):
    return re.sub(
        r'\b(CONCEPTES GENERALS|EPIDEMIOLOGIA|ETIOPATOGÈNIA|DIAGNÒSTIC|CLÍNICA|PREVENCIÓ|TRACTAMENT|PRINCIPIS ACTIUS|ENTORN SOCIAL)\.(?!@)',
        lambda m: f'\n{m.group(1)}.@',
        texto,
        flags=re.UNICODE
    )



def marca_entrada(texto):
    linhas = texto.splitlines()
    output = []

    # Regex para capturar o número no início e a estrutura típica da entrada
    padrao = re.compile(
        r'(?<!-)\b(\d{1,3})(\s+\w+.*?\s(?:pl|n|m|f|adj|sigla|\||tr))\s*$',
        flags=re.UNICODE
    )

    for linha in linhas:
        match = padrao.search(linha.strip())
        if match:
            numero, resto = match.groups()
            nova_linha = linha.replace(f"{numero}{resto}", f"«{numero}{resto}")
            output.append(nova_linha)
        else:
            output.append(linha)

    return '\n'.join(output)






def casos_especiais(texto):
    linhas_marca_extra = [5629, 5632, 5633, 5634, 5635, 5636, 5626, 5668,5723,5779,5834,5836,5857]
    linhas_adicionar_marca = [3533,8620,12129,6752]

    texto_linhas = texto.splitlines()

    # Corrige linhas com marca a mais (procura e remove apenas a primeira ocorrência de «)
    for linha in linhas_marca_extra:
        idx = linha - 1
        if '«' in texto_linhas[idx]:
            texto_linhas[idx] = texto_linhas[idx].replace('«', '', 1)

    # Adiciona marca à linha 3533, se ainda não tiver
    for linha_adicionar_marca in linhas_adicionar_marca:
        idx_adicionar = linha_adicionar_marca - 1
        if '«' not in texto_linhas[idx_adicionar]:
            texto_linhas[idx_adicionar] = '«' + texto_linhas[idx_adicionar]

    return '\n'.join(texto_linhas)


    
    



def contar_marcas(texto):
    # Contar o número de @ no texto
    count_at = len(re.findall(r'@', texto))

    # Contar o número de « no texto
    count_les = len(re.findall(r'«', texto))

    return count_at, count_les


def marca_texto(path_texto):    #quase completo
    with open(path_texto, "r", encoding="utf-8") as f_in:
        texto = f_in.read()

    texto_def = marca_def(texto)
    texto_num = marca_entrada(texto_def)
    texto_completo = casos_especiais(texto_num)


    print(contar_marcas(texto_completo))
    

    with open(path_texto, "w", encoding="utf-8") as f_out:
        f_out.write(texto_completo)



marca_texto('processamento_dic\diccionari_layout_alterado.txt')

#definição é o que está entre o @ e o «-- ;)






    

#--------------------------------------------------------------------------------------------------------------------
# associar definicao a conceito
 
 # ENCONTRAR DEFINICAO, com identificador associado

 #dividir por blocos e formar dicinoario: conceito : definição



def dividir_blocos(path_texto):
    with open(path_texto, "r", encoding="utf-8") as f_in:
        texto = f_in.read()

    partes = texto.split('«')
    dicionario = {}

    for parte in partes:
        parte = parte.strip()
        if not parte:
            continue

        # Extrai o número original
        numero_match = re.match(r'^(\d+)', parte)
        if not numero_match:
            continue
        numero = numero_match.group(1)

        # Tenta extrair definição
        definicao_match = None
        if '@' in parte:
            definicao_match = re.search(r'@(.+?)(?=\n\d|$)', parte, re.DOTALL)
        elif 'veg.' in parte:
            definicao_match = re.search(r'(veg\..+?)(?=\n\d|$)', parte, re.DOTALL)
        else:
            # Captura alternativa para últimas definições
            definicao_match = re.search(r'([a-zA-ZçÇàáéíóúè]+.+?)(?=\n\d|$)', parte, re.DOTALL)

        if definicao_match:
            definicao = definicao_match.group(1).strip().replace('\n', ' ')
            dicionario[numero] = definicao
        else:
            dicionario[numero] = ""  # sem definição

 

    with open('processamento_dic/dic_definicoes.json', "w", encoding="utf-8") as f_out:
        json.dump(dicionario, f_out, ensure_ascii=False, indent=2)

    return dicionario





dividir_blocos('processamento_dic\diccionari_layout_alterado.txt')




