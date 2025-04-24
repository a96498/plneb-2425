import re
import json
import pprint
import unicodedata


def tratamento():
    file = open('processamento_glossario_popular\Glossário de Termos Médicos Técnicos e Populares.pdf.txt', 'r', encoding='utf8')
    glossario = open("glossario.txt", "w", encoding='utf8')

    texto=file.read()

    texto=re.sub(r"\f","",texto) #tira as quebras de pagina
    texto=re.sub(r"\n\n","\n",texto) #poe_todo o texto corrido
    texto = re.sub(r"\s*[,;]\s*", ",", texto)  # ficar tudo normalizado


    linhas = texto.splitlines()
    bloco=''
    letra_indice=''

    for i,line in enumerate(linhas):

        if re.fullmatch(r"^[A-Z]$",line) :
            bloco= f"{bloco}{line}\n"
            letra_indice = line.lower()

        else:

            if letra_indice == '':
                continue

            elif unicodedata.normalize('NFD', line[0].lower())[0] == letra_indice:
                line = re.sub(rf"^{line[0]}",rf"@{line[0]}",line)  #cada linha de conceito é marcada por @ porque existem conceitos que estão quebrados a meio
                bloco= f"{bloco}{line}\n"

            else:
                bloco = f"{bloco}{line}\n"




    glossario.write(bloco)


    file.close()
    glossario.close()




def glossario(): #secalhar somehow meter as palavras a negrito como keys?
    file = open('processamento_glossario_popular\glossario.txt', 'r', encoding='utf8')
    entradas = re.findall(r"@.+",file.read())
    dic={}
    for conceito in entradas:
        definicoes = conceito.split(",")
        lista=[]

        for ind, definicao in enumerate(definicoes):

            definicao = re.sub(r"@", "", definicao)

            if "(pop)" in definicao:
                #print(definicao)
                pal_popular = re.sub(r" \(pop\)","",definicao)
                pal_popular = pal_popular.strip('()[]\\"')

                pal_popular=pal_popular.strip()


            else:


                lista.append(definicao.strip())

        if pal_popular in dic:

            dic[pal_popular].extend(lista)
        else:
            dic[pal_popular] = lista

    for key in dic.keys():
        dic[key] = list(set(dic[key]))

    dic_ordenado = dict(sorted(dic.items()))

    file_out = open('glossario.json', 'w', encoding='utf8')
    json.dump(dic_ordenado, file_out, ensure_ascii=False, indent=4)
    file_out.close()

    return dic_ordenado

#existe um stress com uma cena que é so aparecer (pop), secalhar tiro? nem percebo mt bem oq é suposto ser




def adicionar_glossario():
    db_file = open(r"processamento_glossario_popular\neologismos_final.json", encoding="utf8")
    db = json.load(db_file)
    db_file.close

    dic = glossario()

    stopwords = [
    "a", "à", "ao", "aos", "as", "àquela", "àquelas", "àquele", "àqueles", "aquilo", "aquela", "aquelas", "aquele", "aqueles",
    "com", "como", "da", "das", "de", "dela", "delas", "dele", "deles", "do", "dos", "em", "entre", "essa", "essas", "esse",
    "esses", "esta", "estas", "este", "estes", "eu", "ele", "ela", "eles", "elas", "foi", "foram", "fui", "há", "isso", "isto",
    "já", "lhe", "lhes", "mais", "mas", "me", "mesmo", "meu", "meus", "minha", "minhas", "muito", "na", "nas", "nem", "no", "nos",
    "nós", "nossa", "nossas", "nosso", "nossos", "num", "numa", "nunca", "o", "os", "ou", "para", "pela", "pelas", "pelo", "pelos",
    "por", "qual", "quando", "que", "quem", "se", "sem", "seu", "seus", "só", "sua", "suas", "também", "te", "tem", "têm", "tenho",
    "tinha", "tive", "tu", "tua", "tuas", "um", "uma", "você", "vocês", "vos", "e", "não", "ser", "está", "estão", "estava",
    "estavam", "estivemos", "estiveram", "estivesse", "estivessem", "fazia", "faz", "fazem", "fazer", "são", "era", "eram",
    "sou", "serei", "seria", "seriam", "seja", "sejam", "tenha", "tenham", "ter", "terei", "teria", "teriam", "tinha", "tinham", "que"
]


    for entrada in db:
        conceito = entrada.get('conceito','')
        significado = entrada.get('significado','')
        contexto = entrada.get('contexto','')


        for exp_pop in dic.keys():

            if exp_pop in stopwords:
                continue

            if (re.search(rf'\b{re.escape(exp_pop)}\b', conceito, re.IGNORECASE) or
                    re.search(rf'\b{re.escape(exp_pop)}\b',significado, re.IGNORECASE) or re.search(rf'\b{re.escape(exp_pop)}\b',contexto, re.IGNORECASE)):


                if f"outras associacoes a '{exp_pop}'" not in entrada.keys():
                    terminologias = dic[exp_pop]
                    #terminologias.append(exp_pop)

                    entrada[f"outras associacoes a '{exp_pop}'"] = list(set(terminologias))

                else:
                    terminologias = entrada[f"outras associacoes a '{exp_pop}'"]
                    #terminologias.append(exp_pop)
                    terminologias.extend(dic[exp_pop])

                    entrada[f"outras associacoes a '{exp_pop}'"] = list(set(terminologias))

            for exp in dic[exp_pop]:

                if exp in stopwords:
                    continue

                if re.search(rf'\b{re.escape(exp)}\b', conceito, re.IGNORECASE) or re.search(rf'\b{re.escape(exp)}\b',significado, re.IGNORECASE) or re.search(rf'\b{re.escape(exp)}\b',contexto, re.IGNORECASE):

                    if f"outras associacoes a '{exp}'" not in entrada.keys():
                        terminologias = dic[exp_pop]
                        terminologias.remove(exp)
                        terminologias.append(exp_pop)
                        #print(list(set(terminologias)))

                        entrada[f"outras associacoes a '{exp}'"] = list(set(terminologias))

                    else:
                        terminologias = entrada[f"outras associacoes a '{exp}'"]
                        terminologias.append(exp_pop)
                        terminologias.extend(dic[exp_pop])
                        terminologias.remove(exp)
                        #print(list(set(terminologias)))

                        entrada[f"outras associacoes a '{exp}'"] = list(set(terminologias))

    with open("processamento_glossario_popular\gloss_final.json", 'w', encoding="utf8") as db_file:
        json.dump(db, db_file, ensure_ascii=False, indent=4)








adicionar_glossario()