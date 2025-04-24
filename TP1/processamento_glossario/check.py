import json

# Caminho para o ficheiro JSON
ficheiro_json = r"processamento_glossario\neologismos_final.json"

# Ler o conteúdo do ficheiro JSON
with open(ficheiro_json, 'r', encoding='utf-8') as f:
    conceitos = json.load(f)

# Verificar os campos sem "tradução_esp"
conceitos_sem_traducao_esp = [
    conceito["conceito"] for conceito in conceitos
    if "tradução_esp" not in conceito or not conceito["tradução_esp"].strip()
]

# Resultado
if conceitos_sem_traducao_esp:
    print("Conceitos sem tradução_esp:")
    for c in conceitos_sem_traducao_esp:
        print(c)