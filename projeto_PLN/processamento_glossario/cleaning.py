import re

caminho_ficheiro = r"processamento_glossario\neologismos.xml"
caminho_ficheiro_clean = r"processamento_glossario\neologismos.xml"

# LIMPEZA XML
with open(caminho_ficheiro, encoding="utf-8") as file:
    texto = file.read()

# Remover o cabeçalho XML
texto = re.sub(r'^.*?<b>3\.2\. O glossário </b></text>', '', texto, flags=re.DOTALL)
# Remover o rodapé XML
texto = re.sub(r'<page number="184".*$', '', texto, flags=re.DOTALL)
# Remover tags XML
texto = re.sub(r'<.*?>', '', texto)
# Remover referências em contextos (ex: (p. 123, 456))
texto = re.sub(r'\s*\(\d+(?:,\s*\d+)*\)', '', texto)

# Adição de TAGS
# conceitos=@ ; traduções=»; significado=*; significado enciclopédico=«; contexto=£; 
# Substituir 's.f.' ou 's.m.' por '@' (logo após o nome do conceito) 
texto = re.sub(r'\n([^\n]+)\n\s*s\.f\.\s*\n', r'\n@\1\n', texto, flags=re.IGNORECASE) #colocar o @ no início da linha
texto = re.sub(r'\n([^\n]+)\n\s*s\.m\.\s*\n', r'\n@\1\n', texto, flags=re.IGNORECASE)

# Traduções
# É necessário certificar que se mantêm-na mesma linha
texto = re.sub(r'(@[^\n]+)\n', r'\1\n» ', texto) #coloca uma tag no início do significado o \1 mantem o [esp] e o $\2 coloca o $ no início da linha seguinte (o significado) 
#dois termos que não se aplicam @ está mal editado de raiz e falta [esp] (está escrito [es apenas)

# Início do significado
texto = re.sub(r'(\[esp\].*\n+)([^\n])', r'\1*\2', texto) 

# Significado enciclopédico
texto = re.sub(r'Inf\.\s*encicl\.: ', '«', texto)

# Contexto
texto = re.sub(r'\n*“', r'\n£“', texto)

texto = re.sub(r'(?<=\S)\n+', ' ', texto)  # Substitui quebras de linha por espaços apenas entre palavras


# Guardar
with open(caminho_ficheiro_clean, "w", encoding="utf-8") as file:
    file.write(texto)




