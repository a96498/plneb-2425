titulo = 'Bolo do Faísca McQueen'
subtitulo = 'Tutorial passo a passo'
subsubtitulo = 'Katchow!!'

Passo1 = "Encontrar receita de bolo do seu agrado, e fazer! Para seguir este método, precisamos de um bolo grande e dois bolos mais pequenos."

Passo2 = "Desenformar os bolos, e cortar o grande segundo a forma da base do carro."

Passo3 = "Utilizar um bolo dos pequenos e o necessário do segundo para a parte de cima do carro. Com o restante, fazer os restantes detalhes: faróis, alarão e detalhes na parte de trás. Se possível, utilizar morangos picados finamete e natas para colar os dois andares. Se achar conveniente, colocar palitos para garantir uma estrutura sólida."

Passo4 = "Hora da Cobertura! Bater um pacote de natas e cortar morangos bem vermelhos às fatias."

Passo5 = "Cobrir o bolo com as natas e dispor os morangos de maneira a cobrir a maior área possível. \nNa zona dos olhos, não colocar morangos. Em vez disso, colocar uma avelã em cada olho.\nPara fazer as rodas, utilizar as bolachas redondas mais escuras que tiver "

Conclusao = 'Tchanaaaaaaa!!!! Aniversariante feliz :)'


html_content = f"""
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>

</head>
<body>
    <h1><p style="text-align: center;color: red;">{titulo}</p></h1>
    <h2><p style="text-align: center;">{subtitulo}</p></h2>
    <h3><p style="text-align: center;color: red;">{subsubtitulo}\n\n</p></h3>

    <p style="text-align: center;"><img src="vistas.jpg"  width="300"></p>


    <h4><strong>\nPasso 1</strong></h4>
    <img src="fazer_bolos.jpg"  width="300">
    <h5>{Passo1}\n</h5>


    <h4><strong>\nPasso 2</strong></h4>
    <img src="desenformar_bolos.jpg"  width="300">
       <img src="cortar_bolos.jpg"  width="300">
<h5>{Passo2}\n</h5>
    
    <h4><strong>\nPasso 3</strong></h4>
    <img src="bolo_nu.jpg"  width="300">
    <h5>{Passo3}\n</h5>

    <h4><strong>\nPasso 4</strong></h4>
    <h5>{Passo4}\n</h5>
    
    <h4><strong>\nPasso 5</strong></h4>
    <img src="bolo_vermelho.jpg"  width="300">
    <h5>{Passo5}\n</h5>
        
    <h4><strong>\nPasso 6</strong></h4>
    <img src="aniversariante.jpg"  width="300">
    <h5>{Conclusao}\n</h5>

</body>
</html>
"""

# Criar e escrever no ficheiro HTML
with open("tpc_html\mcQueen.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("Ficheiro HTML gerado com sucesso!")
