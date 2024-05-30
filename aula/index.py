from flask import Flask, redirect,render_template, request, flash, session

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# a linha abaixo cria uma chave de segurança
app.secret_key = 'aprendendodoiniciocomdaniel'

#** a linha abaixo configura o acesso ao banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector', 
        usuario = 'aluno',
        senha = 'toor',
        servidor = 'localhost',
        database = 'loja'
    )

# a linha abaixo cria uma instancia com a SQLALCHEMY
db = SQLAlchemy(app)

class Produto(db.Model):
      id_produto = db.Column(db.Integer, primary_key=True,autoincrement=True)
      nome_produto = db.Column(db.String(50), nullable=False)
      marca_produto = db.Column(db.String(40), nullable=False)
      preco_produto = db.Column(db.Float, nullable=False)

      def __repr__(self):
            return '<Name %r>' % self.name

#Linha acima configura o acesso ao usuário

@app.route('/inicio')
def ola():
        return'<h1> Iniciando flask</h1>'


@app.route('/lista')
def lista():
        # sem login sem acao (n vai abrir o lista)
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
         return redirect('/login')

    produtos_cadastrados = Produto.query.order_by(Produto.id_produto)
       
    return render_template('lista.html', descricao = "aqui estão os seus produtos cadastrados",
                               lista_prod = produtos_cadastrados)

@app.route('/cadastrar' )
def cadastrar_produto():
    return render_template('cadastrar.html')

@app.route('/adiciona',methods=['POST',] )
def adicionar_produto():

    # as variaveis abaixo recebem as informações digitadas pelo user.
    nome_prod = request.form ['txtNome']

    marca_prod = request.form ['txtMarca']

    #a linha abaixo altera o ',' por '.'

    preco_prod = request.form['txtPreco'].replace(',','.') #replace vai alterar algo ('ISSO',"PORISSO")
    #linha abaixo converte o valor digitado pelo user.
    preco_prod = float(preco_prod)

    produto_adicionado = Produto(nome_produto= nome_prod, marca_produto = marca_prod, preco_produto=preco_prod)
    #linha abaixo é feitp um preparo pro envio ao banco de dados

    db.session.add(produto_adicionado)
    #na linha de baixo envia para o banco de dados
    db.session.commit()

    flash(" Produto cadastrado com sucesso!!")
    #importar o flash
    return redirect('/lista')
# aq inicia a parte da edicao do produto:
 
@app.route('/editar/<int:id>') # rota preparada para recebeer um id
def editar_produto(id):   #sinal da maior e menor, id's diferentes, se não colocar, será igual pra todos
    
    # a linha abaixo trás o produto selecionado pra ser atualizado
    produto_selecionado = Produto.query.filter_by(id_produto=id).first() #filter.by foltrar id especifico
    return render_template('editar.html', produto = produto_selecionado)

@app.route('/atualizar' , methods=['POST', ])
def atualiza_registro():
     
    # linha abaixo garante a atualização
    produto = Produto.query.filter_by(id_produto=request.form['txtId']).first()
        #linhas abaixo altera os campos no banco dados
    produto.nome_produto = request.form['txtNome'] #variavel usada no editar.html
    produto.marca_produto = request.form['txtMarca']
    produto.preco_produto = request.form['txtPreco']
    #produto = nome do banco dados; preco_produto nome dos dados tabela



    #linha abaixo adiciona a atualização do protudo (update)
    db.session.add(produto)

    #linha abaixo envia as infos para a tabela do banco
    db.session.commit()
    flash(" Produto atualizado com sucesso!!")
    return redirect('/lista')

#A LINHA ABAIXO É INICIADO A PARTE DE EXCLUIR DADOS
@app.route('/excluir/<int:id>')
def excluir_produto(id):
     
# a linha abaixo exclui o registro
     Produto.query.filter_by(id_produto=id).delete()
                            #tem crtza q o id selecionado so vai excluir o id do banco
     # a linha abaixo sobe a exclusão para o banco
     db.session.commit() 
     flash(" Produto excluido com sucesso!!")

     return redirect('/lista')
# a linha abaixo cria a rota paraa o login

@app.route('/login')
def login():
     
   return render_template ('login.html')

@app.route('/autenticar', methods=['post' ,]) #essa virgula = só essa parte
def autenticar():
     login = request.form['txtLogin']
     senha = request.form['txtSenha']

     if login == 'admin' and senha == 'admin':
          #*** Importante:
            # para criar a sessão do usuario é necessário ter
            # iniciado a propriedade secret_key
            # ela garante que seja mapeado o hash do usuario
            # enquantoa a aplicacao esteja sendo executada
        # session deve ser importado no import do flask 
        session['usuario_logado'] = login
        flash("usuario logado com sucesso")

        return redirect("/lista")
     else:
        return redirect('/login')

app.run()

# pip install flask

