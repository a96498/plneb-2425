import json

def junta_dicionario_glossario(dicionario, glossario, path_doc_novo):
    # Carrega os arquivos
    with open(dicionario, 'r', encoding='utf-8') as f:
        lista_dic = json.load(f)

    with open(glossario, 'r', encoding='utf-8') as f:
        lista_gloss = json.load(f)

    # Cria dicionário de glossário
    gloss_dict = {}
    for item in lista_gloss:
        if 'conceito' in item:
            gloss_dict[item['conceito']] = item

    # Indexa o dicionário principal por conceito
    dic_dict = {}
    for entrada in lista_dic:
        conceito = entrada.get('conceito')
        if conceito:
            dic_dict[conceito] = entrada

    # Processa as entradas
    resultado = []
    conceitos_processados = set()
    conceitos_comuns = 0

    for conceito, entrada_dic in dic_dict.items():
        novo_item = {
            'conceito': conceito
        }

        # Adiciona todos os dados do dicionário
        for k, v in entrada_dic.items():
            if k != 'conceito':
                novo_item[k] = v

        # Se existir no glossário, mescla os dados
        if conceito in gloss_dict:
            conceitos_comuns += 1
            dados_gloss = gloss_dict[conceito]
            for k, v in dados_gloss.items():
                if k not in novo_item:
                    novo_item[k] = v

        resultado.append(novo_item)
        conceitos_processados.add(conceito)

    # Agora adiciona conceitos que estão só no glossário
    for conceito, dados_gloss in gloss_dict.items():
        if conceito not in conceitos_processados:
            novo_item = {
                'conceito': conceito
            }
            novo_item.update(dados_gloss)
            resultado.append(novo_item)

    # Escreve resultado final
    with open(path_doc_novo, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    #print(f"Número de conceitos em comum entre dicionário e glossário: {conceitos_comuns}")


DICIONARIO = r'processamento_dic\dicionario_final.json'
GLOSSARIO = r'processamento_glossario\neologismos_final.json'
JSON_SEMI_COMPLETO = r'processamento_dic\json_completo.json'

junta_dicionario_glossario(DICIONARIO, GLOSSARIO, JSON_SEMI_COMPLETO)

