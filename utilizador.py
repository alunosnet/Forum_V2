from flask import Flask, render_template,request,redirect, session
from basedados import *
import os
from werkzeug.utils import secure_filename
from flask_session import Session

def login():
    if request.method=="GET":
        return render_template('utilizador/login.html')
    if request.method=="POST":
        #pesquisar na bd o utilizador
        email = request.form.get("email")
        palavra_passe=request.form.get("palavra_passe")
        sql="SELECT * FROM utilizador WHERE email=? AND palavra_passe=?"
        parametros=(email,palavra_passe)
        dados = DevolverSQL(sql,parametros)
        if len(dados)!=1:
            mensagem="O login falhou. Tente novamente."
            return render_template("utilizador/login.html",mensagem=mensagem)
        #iniciar sessão
        #guardar o id, email, nome, perfil
        session["email"]=email
        session["id"]=dados[0]['id']
        session["nome"]=dados[0]['nome']
        session["perfil"]=dados[0]['perfil']
        return redirect("/")

#só para admin
def utilizador_criar(app):
    if request.method=="GET":
        return render_template('utilizador/criar.html')
    if request.method=="POST":
        #recolher os dados do form
        nome = request.form.get("nome")
        email = request.form.get("email")
        palavra_passe = request.form.get("palavra_passe")
        perfil = request.form.get("perfil")
        #validar os dados
        if not nome or not email or not palavra_passe:
            return render_template('utilizador/criar.html',mensagem="Tem de preencher todos os campos")
        
        sql="SELECT * FROM Utilizador WHERE email=?"
        parametros=(email,)
        dados = DevolverSQL(sql,parametros)
        if dados:
            return render_template('utilizador/criar.html',mensagem="O email já existe")

        ficheiro = request.files["fotografia"]
        #nome_ficheiro=secure_filename(ficheiro.filename)
        ficheiro.save(os.path.join(app.config["UPLOAD_FOLDER"],nome))

        #adicionar a bd
        sql="INSERT INTO Utilizador(nome, email, palavra_passe, estado, perfil) values(?,?,?,?,?)"
        parametros=(nome,email,palavra_passe,1,perfil)
        ExecutarSQL(sql,parametros)
        #redirecionar
        return redirect('/utilizador/listar')

def utilizador_registar(app):
    if request.method=="GET":
        return render_template('utilizador/registar.html')
    if request.method=="POST":
        #recolher os dados do form
        nome = request.form.get("nome")
        email = request.form.get("email")
        palavra_passe = request.form.get("palavra_passe")
        #validar os dados
        if not nome or not email or not palavra_passe:
            return render_template('utilizador/registar.html',mensagem="Tem de preencher todos os campos")
        
        sql="SELECT * FROM Utilizador WHERE email=?"
        parametros=(email,)
        dados = DevolverSQL(sql,parametros)
        if dados:
            return render_template('utilizador/registar.html',mensagem="O email já existe")

        ficheiro = request.files["fotografia"]
        #nome_ficheiro=secure_filename(ficheiro.filename)
        ficheiro.save(os.path.join(app.config["UPLOAD_FOLDER"],nome))

        #adicionar a bd
        sql="INSERT INTO Utilizador(nome, email, palavra_passe, estado, perfil) values(?,?,?,?,1)"
        parametros=(nome,email,palavra_passe,1)
        ExecutarSQL(sql,parametros)
        #redirecionar
        return redirect('/utilizador/listar')

def utilizador_listar():
    #consultar a bd para obter a lista de utilizadores
    sql = "SELECT * FROM Utilizador"
    dados = DevolverSQL(sql)
    return render_template('utilizador/listar.html',registos=dados)

def utilizador_apagar():
    #recolher o id do utilizador a apagar
    id = request.form.get("id")
    #consulta à bd para ter os dados do utilizador
    sql = "SELECT * FROM Utilizador WHERE id=?"
    parametros=(id,)
    dados = DevolverSQL(sql,parametros)
    #mostrar a página para confirmar o apagar
    return render_template("utilizador/apagar.html",registo=dados[0])

def utilizador_apagar_confirmado(app):
    #recolher o id do utilizador a apagar
    id = request.form.get("id")
    #apagar fotografia
    nome = request.form.get("nome")
    nome=os.path.join(app.config["UPLOAD_FOLDER"],nome)
    if os.path.exists(nome):
        os.remove(nome)
    #apagar da bd
    sql = "DELETE FROM Utilizador WHERE id=?"
    parametros=(id,)
    ExecutarSQL(sql,parametros)
    #redirecionar para utilizador/listar
    return redirect("/utilizador/listar")

def utilizador_editar():
    id = request.form.get("id")
    sql = "SELECT * FROM Utilizador WHERE id=?"
    parametros=(id,)
    dados = DevolverSQL(sql,parametros)
    return render_template("utilizador/editar.html",registo=dados[0])

def utilizador_editar_confirmado(app):
    #recolher dados do form
    nome = request.form.get("nome")
    email = request.form.get("email")
    password = request.form.get("palavra_passe")
    id = request.form.get("id")
    #validar dados
    if not nome or not email or not password:
        return render_template("utilizador/editar.html",mensagem="Tem de preencher todos os campos")
    
    ficheiro = request.files["fotografia"]
    if ficheiro:
        #testar se escolheu enviar nova foto
        ficheiro.save(os.path.join(app.config["UPLOAD_FOLDER"],nome))
    #atualizar a bd
    sql = "UPDATE Utilizador SET nome=?, email=?, palavra_passe=? WHERE id=?"
    parametros=(nome,email,password,id)
    ExecutarSQL(sql,parametros)
    #voltar à lista
    return redirect("/utilizador/listar")

