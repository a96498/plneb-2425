from flask import Flask, request, render_template
import json
app = Flask(__name__)

# db_file = open("C:\Users\Sofia\OneDrive\Ambiente de Trabalho\PLN\conceitos.json")
db_file = open(r"C:\Users\Sofia\OneDrive\Ambiente de Trabalho\PLN\aula5\conceitos_.json", encoding='UTF-8')

db = json.load(db_file)
db_file.close()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/conceitos")
def conceitos():
    designacoes = list(db.keys())
    return render_template("conceitos.html", designacoes=designacoes, title="Lista de Conceitos")

@app.route("/api/conceitos")
def api_conceitos():
    return db

@app.route("/api/conceitos/<designacao>")
def api_conceito(designacao):

    return {"designacao":designacao, "descricao":db[designacao]}



@app.route("/conceitos/<designacao>")
def conceito_detalhe(designacao):
    if designacao in db:
        return render_template("conceito_comRef.html", designacao=designacao, descricao=db[designacao])
    else:
        return "Conceito não encontrado", 40



@app.post("/api/conceitos")
def adicionar_conceito():
    #json
    data = request.get_json()
    #{"designacao":"vida", "descricao": "a vida é ..."}
    db[data["designacao"]] = data["descricao"]
    f_out = open("conceitos_.json", "w")
    json.dump(db,f_out, indent=4, ensure_ascii=False)
    f_out.close()
    #form data
    return data

app.run(host="localhost", port=4002, debug=True)