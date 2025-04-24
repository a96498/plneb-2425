import re
import json

caminho_ficheiro = r"processamento_glossario\neologismos_final.xml"
caminho_ficheiro_json = r"processamento_glossario\neologismos.xml"

# Ler o conteúdo do ficheiro
with open(caminho_ficheiro, encoding="utf-8") as file:
    texto = file.read()

# 1. Remover as quebras de linha dentro dos parâmetros
texto = re.sub(r'(?<=\S)\n+', ' ', texto)  # Substitui as quebras de linha por espaço

# 2. Criar uma lista para armazenar os conceitos e os parâmetros
conceitos = []

# 3. Separar os conceitos com base na tag @ (que está antes de cada conceito)
conceitos_data = re.split(r'@', texto)[1:]  # Ignora a primeira parte antes do primeiro conceito

for conceito_texto in conceitos_data:
    conceito_dict = {}
    
    # 4. Extrair o nome do conceito (primeira linha após @)
    nome_conceito = conceito_texto.splitlines()[0].strip()
    
    # Adicionar o nome do conceito ao dicionário
    conceito_dict['conceito'] = nome_conceito
    
    # 5. Extrair os parâmetros usando as tags
    traducoes_match = re.search(r'»(.*?)(?=[*«£@]|$)', conceito_texto, flags=re.DOTALL)
    if traducoes_match:
        traducoes_str = re.sub(r'\n+', ' ', traducoes_match.group(1).strip())
        traducoes_lista = [t.strip() for t in traducoes_str.split(';') if t.strip()]

        for traducao in traducoes_lista:
            if '[ing]' in traducao:
                conceito_dict['en'] = traducao.replace('[ing]', '').strip()
            elif '[esp]' in traducao:
                conceito_dict['es'] = traducao.replace('[esp]', '').strip()
        
    significado = re.search(r'\*(.*?)(?=\n[^\n]*[@»£]|$)', conceito_texto, flags=re.DOTALL)
    if significado:
        # Remover quebras de linha dentro do significado
        conceito_dict['significado'] = re.sub(r'\n+', ' ', significado.group(1).strip())

    significado_encicl = re.search(r'«(.*?)(?=\n[^\n]*[@»£]|$)', conceito_texto, flags=re.DOTALL)
    if significado_encicl:
        # Remover quebras de linha dentro do significado enciclopédico
        conceito_dict['significado_enciclopédico'] = re.sub(r'\n+', ' ', significado_encicl.group(1).strip())

    contexto = re.search(r'£(.*?)(?=\n[^\n]*[@»£]|$)', conceito_texto, flags=re.DOTALL)
    if contexto:
        # Remover quebras de linha dentro do contexto
        conceito_dict['contexto'] = re.sub(r'\n+', ' ', contexto.group(1).strip())
        # Remover aspas do contexto
        conceito_dict['contexto'] = conceito_dict['contexto'].replace('“', '').replace('”', '')

    # Adicionar o conceito e os parâmetros à lista
    conceitos.append(conceito_dict)

# 6. Converter a lista de conceitos em JSON e salvar no arquivo
with open(caminho_ficheiro_json, 'w', encoding='utf-8') as json_file:
    json.dump(conceitos, json_file, ensure_ascii=False, indent=4)