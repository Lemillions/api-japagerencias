from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb+srv://lemillions:123456abc@cluster0.esrnj.mongodb.net/Japagerencias")
db = client['Japagerencias']
usuarios = db['usuarios']
produto = db['produtos']

    
@app.route('/', methods=['GET', 'POST'])
def login():
  if(request.method == "POST"): 
    queryUser = str(request.json["user"])
    querySenha = str(request.json["senha"])
    resultado = usuarios.find_one({"usuario":queryUser,"senha":querySenha}  )
    if(str(resultado) == "None"):
      return "Errado"
    else:
      return {"usuario": resultado["usuario"],
              "permisao": resultado["permissao"],
              "historico": resultado["historico"]}
  else:
    return "Oi"

@app.route('/produtos', methods=['GET', 'POST'])
def produtos():
  if(request.method == "GET"):
    todosProdutos = []
    produtosLista = produto.find({},{'_id':0});
    for x in produtosLista:
      todosProdutos.append(x)
    return jsonify(todosProdutos)

  elif(request.method == "POST"):
    queryProdutoOriginal = {"nome" : request.json['original']}
    novoValorDoProduto = { "$set": { "nome": request.json['nome'], "quantidade": request.json['quantidade'], "valor": request.json['valor'] } }
    produto.update_one(queryProdutoOriginal, novoValorDoProduto)
    todosProdutos = []
    novosProdutos = produto.find({},{'_id':0})
    for x in novosProdutos:
      todosProdutos.append(x)
    return jsonify(todosProdutos)
  else:
    return "oi"


@app.route('/adicionarProduto', methods=['POST'])
def novoProduto():
  if(request.method == "POST"):
    novoNome = request.json["nome"]
    novoQuant = request.json["quantidade"]
    novoValor = request.json["valor"]
    novoProduto = {"nome":novoNome,"quantidade":novoQuant,"valor":novoValor}
    produto.insert_one(novoProduto)
    todosProdutos = []
    novosProdutos = produto.find({},{'_id':0})
    for x in novosProdutos:
      todosProdutos.append(x)
    return jsonify(todosProdutos)
  else:
    return "oi"

@app.route('/comprar', methods=['POST'])
def realizarCompra():
  if(request.method == "POST"):
    historico = []
    historico = usuarios.find_one({"usuario":request.json[1]})['historico']
    print(request.json[0][0])
    usuario = {"usuario":request.json[1]}
    print(historico)
    historico.append(request.json[0][0])
    usuarios.update_one(usuario, { "$set":{"historico":historico}})
    return str(request)
  else:
    return "oi"
  

  
app.run('0.0.0.0')
