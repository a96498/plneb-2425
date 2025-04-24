import re
import json




def tira_num_pags(texto):
    texto = re.sub(r'\f\d{1,3}', '', texto)
    linhas = texto.splitlines()
    texto_sem_primeira = "\n".join(linhas[1:])
    return texto_sem_primeira



PATH_entrada = 'processamento_dic\index_pt.txt'
PATH_saida = 'processamento_dic\index_pt_alterado.txt'

cabecalho = r'Índex portuguès\n\n'

def limpa_index(entrada, saida, cabecalho):
    with open(entrada, "r", encoding="utf-8") as f:
        texto = f.read()

    texto = tira_num_pags(texto)
    texto = re.sub(r'QUADERNS 50 DICCIONARI MULTILINGÜE DE LA COVID-19', '', texto)
    texto = re.sub(r'\u202b', '', texto, flags=re.UNICODE)
    texto = re.sub(r'\u202c', '', texto, flags=re.UNICODE)
    texto = re.sub(cabecalho, '', texto)

    linhas = texto.splitlines()
    novo_texto = []
    buffer = ""

    for i in range(len(linhas)):
        linha = linhas[i].strip()

        if not linha:
            continue

        if re.search(r',\s*\d{1,3}', linha):
            linha_completa = buffer + " " + linha if buffer else linha
            novo_texto.append(linha_completa.strip())
            buffer = ""
        else:
            buffer = linha

    with open(saida, "w", encoding="utf-8") as f:
        for linha in novo_texto:
            f.write(linha + "\n")

def cria_dicionario(PATH_saida):
    with open(PATH_saida, "r", encoding="utf-8") as f:
        conceitos = f.readlines()

    dic = {}

    for linha in conceitos:
        linha = linha.strip()

        if ',' not in linha:
            continue

        conceito, indice = linha.rsplit(',', 1)
        conceito = conceito.strip()
        paginas = re.findall(r'\d+', indice)

        for pag in paginas:
            try:
                pag_int = int(pag)
                if pag_int not in dic:
                    dic[pag_int] = set()
                dic[pag_int].add(conceito)
            except ValueError:
                print(f"Erro ao processar página: {pag} na linha: {linha}")

    return dic

def escreveJSON(PATH_index, dic):
    # Converte set para lista para poder serializar em JSON
    dic_convertido = {pag: sorted(list(conceitos)) for pag, conceitos in dic.items()}

    with open(PATH_index, "w", encoding="utf-8") as f:
        json.dump(dic_convertido, f, ensure_ascii=False, indent=2)




# --- Execução ---
limpa_index(PATH_entrada, PATH_saida, cabecalho)

dic = cria_dicionario(PATH_saida)
#print(f"Entradas encontradas no índice: {len(dic)}")

PATH_indexPT = 'processamento_dic\indexPT.json'
escreveJSON(PATH_indexPT, dic)
