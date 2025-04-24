import os
import re
import json
from index import limpa_index, cria_dicionario, escreveJSON

# ----------------------------------------
# 1. Criação de dicionários por língua
# ----------------------------------------

def cria_dicionarios_linguas():
    linguas = [
        ('processamento_dic/linguas/txt/index_ar.txt', r'Índex àrab\n\n'),
        ('processamento_dic/linguas/txt/index_en.txt', r'Índex anglès\n\n'),
        ('processamento_dic/linguas/txt/index_eu.txt', r'Índex basc\n\n'),
        ('processamento_dic/linguas/txt/index_es.txt', r'Índex castellà\n\n'),
        ('processamento_dic/linguas/txt/index_fr.txt', r'Índex francès\n\n'),
        ('processamento_dic/linguas/txt/index_gl.txt', r'Índex gallec\n\n'),
        ('processamento_dic/linguas/txt/index_nl.txt', r'(Índex neerlandès\n\n|Índex portuguès\n\n)'),
        ('processamento_dic/linguas/txt/index_oc.txt', r'(Índexs bilingües\n\n|Índex occità\n\n)')
    ]

    pasta_base_txt = os.path.join("processamento_dic", "linguas", "txt")
    pasta_base_json = os.path.join("processamento_dic", "linguas", "json")
    os.makedirs(pasta_base_txt, exist_ok=True)
    os.makedirs(pasta_base_json, exist_ok=True)

    for path, cabecalho in linguas:
        if not os.path.exists(path):
            print(f"Arquivo não encontrado: {path}")
            continue

        nome = os.path.basename(path)
        caminho_temp = os.path.join(pasta_base_txt, f"_temp_{nome}")

        with open(path, "r", encoding="utf-8") as f_in, open(caminho_temp, "w", encoding="utf-8") as f_out:
            f_out.write(f_in.read())

        limpa_index(caminho_temp, path, cabecalho)
        os.remove(caminho_temp)

        dicionario = cria_dicionario(path)
        codigo = nome.split("_")[1].replace(".txt", "")
        nome_json = os.path.join(pasta_base_json, f"dic_{codigo}.json")
        escreveJSON(nome_json, dicionario)


# ----------------------------------------
# 2. Criação dos dicionários por área
# ----------------------------------------

def cria_json_areas():
    areas_path = os.path.join("processamento_dic", "areas", "indice_areas.txt")
    with open(areas_path, "r", encoding="utf-8") as f:
        texto = f.read()

    padrao = re.compile(
        r'\n(Conceptes generals|Epidemiologia|Etiopatogènia|Diagnòstic|Clínica|Prevenció|Tractament|Principis actius|Entorn social)\n',
        flags=re.UNICODE
    )

    partes = re.split(padrao, texto)
    dicionario_areas = {}
    for i in range(1, len(partes), 2):
        titulo = partes[i]
        conteudo = partes[i + 1].strip()
        dicionario_areas[titulo] = conteudo

    pasta_txt = os.path.join("processamento_dic", "areas", "txt")
    pasta_json = os.path.join("processamento_dic", "areas", "json")
    os.makedirs(pasta_txt, exist_ok=True)
    os.makedirs(pasta_json, exist_ok=True)

    for area, conteudo in dicionario_areas.items():
        nome_ficheiro = re.sub(r"[^\w]", "_", area.lower()) + ".txt"
        caminho_txt = os.path.join(pasta_txt, nome_ficheiro)

        with open(caminho_txt, "w", encoding="utf-8") as f:
            f.write(conteudo)

        limpa_index(caminho_txt, caminho_txt, "")
        dicionario = cria_dicionario(caminho_txt)

        nome_json = os.path.join(pasta_json, f"dic_{nome_ficheiro.replace('.txt', '')}.json")
        escreveJSON(nome_json, dicionario)


# ----------------------------------------
# 3. Criação do dicionário final
# ----------------------------------------

def cria_dicionario_final(index_pt_path, linguas_dicts, areas_dicts, output_path):
    with open(index_pt_path, 'r', encoding='utf-8') as f:
        index_pt = json.load(f)

    num_para_conceito = {int(k): v for k, v in index_pt.items()}

    linguas_data = {}
    for dic_path in linguas_dicts:
        lingua = os.path.splitext(os.path.basename(dic_path))[0].replace("dic_", "")
        with open(dic_path, 'r', encoding='utf-8') as f:
            linguas_data[lingua] = json.load(f)

    conceito_para_area = {}
    definicoes_dict = {}

    for dic_path in areas_dicts:
        nome_area = os.path.splitext(os.path.basename(dic_path))[0].replace("dic_", "")
        with open(dic_path, 'r', encoding='utf-8') as f:
            dic_area = json.load(f)

        if nome_area == "definicoes":
            definicoes_dict = dic_area
            continue

        for numero_str in dic_area:
            numero = int(numero_str)
            conceito = num_para_conceito.get(numero)
            if conceito:
                if isinstance(conceito, list):
                    for c in conceito:
                        conceito_para_area.setdefault(c, nome_area)
                else:
                    conceito_para_area.setdefault(conceito, nome_area)

    lista_final = []
    for num_str, conceito in index_pt.items():
        num = int(num_str)
        entrada = {}

        if isinstance(conceito, list):
            entrada["conceito"] = conceito[0]
            if len(conceito) > 1:
                entrada["sinónimos pt"] = conceito[1:]
        else:
            entrada["conceito"] = conceito

        for lingua, dic_lingua in linguas_data.items():
            traducao = dic_lingua.get(str(num))
            if traducao:
                entrada[lingua] = traducao

        if isinstance(conceito, list):
            for c in conceito:
                if c in conceito_para_area:
                    entrada["área médica"] = conceito_para_area[c]
                    break
        else:
            if conceito in conceito_para_area:
                entrada["área médica"] = conceito_para_area[conceito]

        definicao = definicoes_dict.get(num_str)
        if definicao:
            entrada["definicao catalã"] = definicao

        lista_final.append(entrada)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(lista_final, f, ensure_ascii=False, indent=2)


# ----------------------------------------
# 4. Executar tudo
# ----------------------------------------

cria_dicionarios_linguas()
cria_json_areas()

PATH_PRINCIPAL = os.path.join('processamento_dic', 'indexPT.json')

DICIONARIOS_LINGUAS = [
    os.path.join("processamento_dic", "linguas", "json", f)
    for f in os.listdir(os.path.join("processamento_dic", "linguas", "json"))
    if f.endswith(".json")
]

DICIONARIOS_AREAS = [
    os.path.join("processamento_dic", "areas", "json", f)
    for f in os.listdir(os.path.join("processamento_dic", "areas", "json"))
    if f.endswith(".json")
]
DICIONARIOS_AREAS.append(os.path.join('processamento_dic', 'dic_definicoes.json'))

PATH_DICIONARIO_FINAL = os.path.join('processamento_dic', 'dicionario_final.json')

cria_dicionario_final(PATH_PRINCIPAL, DICIONARIOS_LINGUAS, DICIONARIOS_AREAS, PATH_DICIONARIO_FINAL)
