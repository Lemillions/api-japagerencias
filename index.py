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

@app.route('/comprar', methods=['GET', 'POST'])
def realizarCompra():
  if(request.method == "POST"):
    historico = []
    historico = usuarios.find_one({"usuario":request.json[1]})['historico']
    usuario = {"usuario":request.json[1]}
    historico.append(request.json[0])
    usuarios.update_one(usuario, { "$set":{"historico":historico}})
    for produtoComprado in request.json[0]["produtos"]:
      queryCompra = {"nome":produtoComprado['nome']}
      quantidadeDoProdutoAtual = int(produto.find_one(queryCompra)['quantidade'])
      quantidadeComprada = int(produtoComprado['quantidade'])
      novaQuantidade = str(quantidadeDoProdutoAtual - quantidadeComprada)
      produto.update_one(queryCompra,{"$set":{"quantidade":novaQuantidade}})
    return str(request)
  else:
    return "oi"

@app.route('/deletar', methods=['POST'])
def deletarProduto():
  query = {"nome":request.json["nome"]}
  produto.delete_one(query)
  return "apagado"
app.run('0.0.0.0')
