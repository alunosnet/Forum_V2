from flask import Flask, render_template,request,redirect
from basedados import *
from datetime import date

#mostrar a mensagem a apagar
def mensagem_apagar():
    id = request.form.get("id")
    parametros = (id,)
    dados = DevolverSQL("SELECT * FROM Mensagem WHERE id=?",parametros)
    return render_template("mensagem/apagar.html",mensagem=dados[0])

#apagar a mensagem e as respostas
def mensagem_apagar_confirmado():
    id = request.form.get("id")
    parametros = (id,)
    sql = "DELETE FROM Mensagem where id_mensagem_original=?"
    ExecutarSQL(sql,parametros)
    sql="DELETE FROM Mensagem WHERE id=?"
    ExecutarSQL(sql,parametros)
    return redirect("/forum")

#Guarda a resposta a uma mensagem do fórum
def mensagem_guardar_resposta():
    id_mensagem_original=request.form.get("id_mensagem_original")
    texto = request.form.get("texto")
    id_utilizador=request.form.get("utilizador")
    #validar dados
    #guardar na bd
    sql = "INSERT INTO Mensagem(id_utilizador,texto,data_hora_mensagem,id_mensagem_original)VALUES(?,?,?,?)"
    data_hora = date.today()
    parametros=(id_utilizador,texto,data_hora,id_mensagem_original)
    ExecutarSQL(sql,parametros)
    #mostrar as respostas à mensagem
    parametros = (id_mensagem_original,)
    texto = DevolverSQL("SELECT * FROM Mensagem WHERE id=?",parametros)
    respostas = DevolverSQL("SELECT * FROM Mensagem WHERE id_mensagem_original=?",parametros)
    utilizadores = DevolverSQL("SELECT id,nome FROM Utilizador ORDER BY Nome")
    return render_template("mensagem/responder.html",mensagem=texto[0],registos=respostas,utilizadores=utilizadores)

#Mostra as respostas de uma mensagem
def mensagem_responder():
    id = request.form.get("id")
    parametros = (id,)
    texto = DevolverSQL("SELECT * FROM Mensagem WHERE id=?",parametros)
    respostas = DevolverSQL("SELECT * FROM Mensagem WHERE id_mensagem_original=?",parametros)
    utilizadores = DevolverSQL("SELECT id,nome FROM Utilizador ORDER BY Nome")
    return render_template("mensagem/responder.html",mensagem=texto[0],registos=respostas,utilizadores=utilizadores)

def mensagem_listar():

    if request.method=="POST":
        #recolher os dados da mensagem
        texto = request.form.get("texto")
        id_utilizador = request.form.get("utilizador")
        #validar os dados
        if texto and id_utilizador:
            #adicionar à tabela das mensagens
            data_atual=date.today()
            sql="INSERT INTO Mensagem(id_utilizador,data_hora_mensagem,texto)VALUES(?,?,?)"
            parametros=(id_utilizador,data_atual,texto)
            ExecutarSQL(sql,parametros)
            mensagem="Mensagem enviada com sucesso"
        else:
            mensagem="Tem de preencher todos os campos"
    else:
        mensagem=""
    #consulta à bd para recolher todas as mensagens iniciais
    sql = "SELECT * FROM Mensagem WHERE id_mensagem_original is null"
    #TODO: join para acrescentar o nome do utilizador
    utilizadores = DevolverSQL("SELECT id,nome FROM Utilizador ORDER BY nome")
    dados = DevolverSQL(sql)
    return render_template("mensagem/index.html",utilizadores=utilizadores,registos=dados,mensagem=mensagem)