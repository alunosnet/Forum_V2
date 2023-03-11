from flask import Flask, render_template,request,redirect
from basedados import *
import os
from werkzeug.utils import secure_filename

#TODO: guardar fotografia
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
        sql="INSERT INTO Utilizador(nome, email, palavra_passe, estado) values(?,?,?,?)"
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

def utilizador_apagar_confirmado():
    #recolher o id do utilizador a apagar
    id = request.form.get("id")
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
    #Francisco vai fazer um aviso para perguntar ao utilizador se quer substituir
    ficheiro.save(os.path.join(app.config["UPLOAD_FOLDER"],nome))
    #atualizar a bd
    sql = "UPDATE Utilizador SET nome=?, email=?, palavra_passe=? WHERE id=?"
    parametros=(nome,email,password,id)
    ExecutarSQL(sql,parametros)
    #voltar à lista
    return redirect("/utilizador/listar")

