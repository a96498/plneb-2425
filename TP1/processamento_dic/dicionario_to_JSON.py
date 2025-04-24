import re
import json
from pathlib import Path

def verifica_arquivo_json(caminho):
    """Verifica se o arquivo JSON existe e é válido"""
    if not Path(caminho).exists():
        raise FileNotFoundError(f"Arquivo {caminho} não encontrado")
    
    with open(caminho, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            raise ValueError(f"Arquivo {caminho} não contém JSON válido")

def tira_num_pags(texto):
    texto = re.sub(r'\f\d{1,3}', '', texto)
    linhas = texto.splitlines()
    texto_sem_primeira = "\n".join(linhas[1:])
    return texto_sem_primeira

def tira_cabecalho(texto):
    texto = re.sub(r'QUADERNS 50 DICCIONARI MULTILINGÜE DE LA COVID-19', '', texto, flags=re.UNICODE)
    texto = re.sub(r'Diccionari\n', '', texto)
    return texto

def tira_letra(texto):
    texto = re.sub(r'\n\w\n\n', '', texto)
    return texto

def coloca_marca(texto):
    linhas = texto.splitlines()
    linhas_marcadas = []

    for linha in linhas:
        if re.match(r'^\d+\s+', linha):
            linha = '@' + linha
        linhas_marcadas.append(linha)

    # Correções manuais
    correcoes = {
        '@35 i 45 cm, d’orelles doblegades': '35 i 45 cm, d’orelles doblegades',
        '@4 hores mitjançant una PCR.': '4 hores mitjançant una PCR.'
    }
    
    linhas_marcadas = [correcoes.get(linha, linha) for linha in linhas_marcadas]
    return "\n".join(linhas_marcadas)

def processa_grava_txt(entrada, saida):
    with open(entrada, "r", encoding="utf-8") as f:
        texto = f.read()

    texto = tira_num_pags(texto)
    texto = tira_cabecalho(texto)
    texto = tira_letra(texto)
    texto = coloca_marca(texto)

    with open(saida, "w", encoding="utf-8") as f:
        f.write(texto)

def extrai_blocos(path_ficheiro):
    with open(path_ficheiro, "r", encoding="utf-8") as f:
        texto = f.read()

    padrao = re.compile(r"\n@(\d{1,3})\s")
    partes = padrao.split(texto)
    dicionario = {}

    for i in range(1, len(partes), 2):
        numero = int(partes[i].strip())
        conteudo = partes[i + 1].strip()
        dicionario[numero] = conteudo

    return dicionario

def encontra_termo_catalao(bloco):
    if not bloco:
        return None
        
    linhas = bloco.splitlines()
    if not linhas:
        return None

    linha = linhas[0]
    partes = re.split(r"\b(n|f|m|adj|sigla|veg\.|sin\. compl\.)\b", linha)
    return partes[0].strip()

def main():
    PATH_entrada = "processamento_dic\diccionari_parcial_raw.txt"
    PATH_saida = "processamento_dic\diccionari_raw_alterado.txt"
    PATH_index = "processamento_dic\indexPT.json"

    try:
        # Processa o arquivo de texto
        processa_grava_txt(PATH_entrada, PATH_saida)
        
        # Extrai os blocos numerados
        dicionario_blocos = extrai_blocos(PATH_saida)
        
        # Carrega o índice em português com verificação
        indice_pt = verifica_arquivo_json(PATH_index)
        
        # Filtra apenas entradas com equivalente em português
        entradas_PT = [int(chave) for chave in indice_pt.keys()]
        dicionario_comPT = {k: v for k, v in dicionario_blocos.items() if k in entradas_PT}
        
        # Processa os termos em catalão apenas para entradas com equivalente PT
        dic_ca = {}
        for k, bloco in dicionario_comPT.items():
            conceito = encontra_termo_catalao(bloco)
            dic_ca[k] = conceito if conceito else ""

        # Guarda o dicionário filtrado com número: conceito
        with open('processamento_dic/linguas/json/dic_ca.json', "w", encoding="utf-8") as f:
            json.dump(dic_ca, f, ensure_ascii=False, indent=2)
            
        #print("Processamento concluído com sucesso!")
        
    except Exception as e:
        print(f"Erro durante o processamento: {str(e)}")

if __name__ == "__main__":
    main()

#print(extrai_blocos())