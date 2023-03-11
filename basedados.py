import sqlite3

BD="Forum.db"

def ExecutarSQL(sql,parametros=None):
    connection = sqlite3.connect(BD)
    if parametros==None:
        connection.execute(sql)
    else:
        connection.execute(sql, parametros)
    connection.commit()
    connection.close()

def DevolverSQL(sql,parametros=None):
    connection = sqlite3.connect(BD)
    connection.row_factory = sqlite3.Row  #isto é para devolver os nomes dos campos
    cursor_object = connection.cursor()
    if parametros==None:
        cursor_object.execute(sql)
    else:
        cursor_object.execute(sql,parametros)
    dados = cursor_object.fetchall()
    connection.close()
    return dados