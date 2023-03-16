from flask import Flask, render_template,request,redirect, session
from basedados import *
import utilizador
import tema
import mensagem
import os
from flask_session import Session

#Criar a bd e as tabelas
tabela_utilizador="create table if not exists utilizador(id integer primary key autoincrement, nome text, email text, palavra_passe text, estado integer, perfil integer)"  #0-admin 1-user
tabela_mensagem="create table if not exists mensagem(id integer primary key autoincrement, texto text, data_hora_mensagem numeric, id_utilizador integer references utilizador(id), id_mensagem_original integer references mensagem(id))"
tabela_tema="create table if not exists tema(id integer primary key autoincrement, nome text, estado integer)"

ExecutarSQL(tabela_utilizador)
ExecutarSQL(tabela_mensagem)
ExecutarSQL(tabela_tema)

#Criar a aplicação Flask
app = Flask(__name__)

app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)

#definir a pasta para guardar ficheiros
UPLOAD_FOLDER=os.path.join(app.root_path,"static/imagens")
app.config["UPLOAD_FOLDER"]=UPLOAD_FOLDER

#Rotas/urls do site
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=["POST","GET"])
def login():
    return utilizador.login()

@app.route('/logout')
def logout():
    session["id"]=None
    session["nome"]=None
    session["email"]=None
    session["perfil"]=None
    return redirect("/")

#rotas da mensagem
@app.route("/mensagem/apagar",methods=["POST"])
def mensagem_apagar():
    if "perfil" not in session:
        return redirect("/login")
    if session["perfil"]!=0:
        return redirect("/login")
    return mensagem.mensagem_apagar()

@app.route("/mensagem/apagar_confirmado",methods=["POST"])
def mensagem_apagar_confirmado():
    if "perfil" not in session:
        return redirect("/login")
    if session["perfil"]!=0:
        return redirect("/login")
    return mensagem.mensagem_apagar_confirmado()

@app.route("/mensagem/guardar_resposta",methods=["POST"])
def mensagem_guardar_resposta():
    if "perfil" not in session:
        return redirect("/login")
    return mensagem.mensagem_guardar_resposta()
    
@app.route("/mensagem/responder",methods=["POST"])
def mensagem_responder():
    if "perfil" not in session:
        return redirect("/login")
    return mensagem.mensagem_responder()

@app.route('/forum',methods=["GET","POST"])
def forum_index():
    if "perfil" not in session:
        return redirect("/login")
    return mensagem.mensagem_listar()

#rotas do tema
@app.route('/tema/adicionar',methods=["GET","POST"])
def tema_adicionar():
    if "perfil" not in session:
        return redirect("/login")
    if session["perfil"]!=0:
        return redirect("/login")
    return tema.tema_adicionar()
    
@app.route('/tema/listar')
def tema_listar():
    if "perfil" not in session:
        return redirect("/login")
    if session["perfil"]!=0:
        return redirect("/login")
    return tema.tema_listar()

@app.route('/tema/apagar',methods=["POST"])
def tema_apagar():
    if "perfil" not in session:
        return redirect("/login")
    if session["perfil"]!=0:
        return redirect("/login")
    return tema.tema_apagar()

@app.route('/tema/apagar_confirmado',methods=["POST"])
def tema_apagar_confirmado():
    if "perfil" not in session:
        return redirect("/login")
    if session["perfil"]!=0:
        return redirect("/login")
    return tema.tema_apagar_confirmado()

@app.route('/tema/editar',methods=["POST"])
def tema_editar():
    if "perfil" not in session:
        return redirect("/login")
    if session["perfil"]!=0:
        return redirect("/login")
    return tema.tema_editar()

@app.route('/tema/editar_confirmado',methods=["POST"])
def tema_editar_confirmado():
    if "perfil" not in session:
        return redirect("/login")
    if session["perfil"]!=0:
        return redirect("/login")
    return tema.tema_editar_confirmado(app)

#Rotas do utilizador
@app.route('/utilizador/criar',methods=["GET","POST"])
def utilizador_criar():
    if "perfil" not in session:
        return redirect("/login")
    if session["perfil"]!=0:
        return redirect("/login")
    return utilizador.utilizador_criar(app)

@app.route('/utilizador/registar',methods=["GET","POST"])
def utilizador_registar():
    return utilizador.utilizador_registar(app)

@app.route('/utilizador/listar')
def utilizador_listar():
    if "perfil" not in session:
        return redirect("/login")
    if session["perfil"]!=0:
        return redirect("/login")
    return utilizador.utilizador_listar()

@app.route('/utilizador/apagar',methods=["POST"])
def utilizador_apagar():
    if "perfil" not in session:
        return redirect("/login")
    if session["perfil"]!=0:
        return redirect("/login")
    return utilizador.utilizador_apagar()

@app.route("/utilizador/apagar_confirmado",methods=["POST"])
def utilizador_apagar_confirmado():
    if "perfil" not in session:
        return redirect("/login")
    if session["perfil"]!=0:
        return redirect("/login")
    return utilizador.utilizador_apagar_confirmado(app)

#rota para editar
@app.route("/utilizador/editar",methods=["POST"])
def utilizador_editar():
    if "perfil" not in session:
        return redirect("/login")
    if session["perfil"]!=0:
        return redirect("/login")
    return utilizador.utilizador_editar()

#rota para atualizar dados
@app.route("/utilizador/editar_confirmado",methods=["POST"])
def utilizador_editar_confirmado():
    if "perfil" not in session:
        return redirect("/login")
    if session["perfil"]!=0:
        return redirect("/login")
    return utilizador.utilizador_editar_confirmado(app)

app.run()