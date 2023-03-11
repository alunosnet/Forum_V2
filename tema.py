from flask import Flask, render_template,request,redirect
from basedados import *

def tema_adicionar():
    if request.method=="GET":
        return render_template('tema/adicionar.html')
    if request.method=="POST":
        #recolher os dados do form
        nome = request.form.get("nome")

        #validar os dados
        if not nome:
            return render_template('tema/adicionar.html',mensagem="Tem de preencher todos os campos")
        
        #adicionar a bd
        sql="INSERT INTO Tema(nome, estado) values(?,?)"
        parametros=(nome,1)
        ExecutarSQL(sql,parametros)
        #redirecionar
        return redirect('/tema/listar')

def tema_listar():
    sql = "SELECT * FROM Tema"
    dados = DevolverSQL(sql)
    return render_template("Tema/listar.html",registos=dados)

def tema_apagar():
    #recolher id
    id = request.form.get("id")
    #consulta a bd para procurar o tema
    sql="SELECT * FROM Tema WHERE id=?"
    parametros=(id,)
    dados = DevolverSQL(sql,parametros)
    #mostrar a página para confirmar o apagar com os dados
    return render_template("tema/apagar.html",registo=dados[0])

def tema_apagar_confirmado():
    #recolher o id do tema a apagar
    id = request.form.get("id")
    #apagar da bd o tema
    sql = "DELETE FROM tema WHERE id=?"
    parametros=(id,)
    ExecutarSQL(sql,parametros)
    #redirecionar para a lista de temas
    return redirect("/tema/listar")

def tema_editar():
     #recolher o id do tema a editar
    id = request.form.get("id")
    #consulta a bd para procurar o tema
    sql = "SELECT * FROM tema WHERE id=?"
    parametros=(id,)
    dados = DevolverSQL(sql,parametros)
    #redirecionar para a lista de temas
    return render_template("/tema/editar.html",registo=dados[0])

def tema_editar_confirmado():
    nome = request.form.get("nome")
    id = request.form.get("id")
    if not nome:
        return render_template("tema/editar.html",mensagem="Tem de preencher todos os campos")
    sql = "UPDATE Tema SET nome=? WHERE id=?"
    parametros=(nome,id)
    ExecutarSQL(sql,parametros)
    return redirect("/tema/listar")