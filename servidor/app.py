import sqlite3
from flask import Flask, g, jsonify, request, url_for
from math import ceil

def dict_factory(cursor, row):
    """Arma un diccionario con los valores de la fila."""
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

def abrirConexion():
    if 'db' not in g:
        g.db = sqlite3.connect("SQL_Sensor.sqlite")
        g.db.row_factory = dict_factory
    return g.db

def cerrarConexion(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

app = Flask(__name__)
app.teardown_appcontext(cerrarConexion)
resultados_por_pag = 10

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/sensor", methods=["POST"])
def sensor():
    db = abrirConexion()  
    datos = request.json
    nombre = datos["nombre"]
    valor = datos["valor"]
    
   
    db.execute("INSERT INTO valores (nombre, valor) VALUES (?, ?)", (nombre, valor))
    

    db.commit()

    cerrarConexion()  

    return jsonify({'resultado': 'OK'})

@app.route("/api/sensores")
def sensores():
    args = request.args
    pagina = int(args.get('page', '1'))
    descartar = (pagina - 1) * resultados_por_pag
    db = abrirConexion()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) AS cant FROM valores;")
    cant = cursor.fetchone()['cant']
    paginas = ceil(cant / resultados_por_pag) if cant else 1

    if pagina < 1 or pagina > paginas:
        cerrarConexion()
        return jsonify({"error": f"Página inexistente: {pagina}"}), 400

    cursor.execute("""SELECT id, nombre, valor FROM valores
                      ORDER BY id DESC
                      LIMIT ? OFFSET ?;""", (resultados_por_pag, descartar))
    lista = cursor.fetchall()
    cerrarConexion()

    siguiente = url_for('sensores', page=pagina+1, _external=True) if pagina < paginas else None
    anterior = url_for('sensores', page=pagina-1, _external=True) if pagina > 1 else None

    info = {
        'count': cant,
        'pages': paginas,
        'next': siguiente,
        'prev': anterior
    }
    res = {'info': info, 'results': lista}
    return jsonify(res)

 




# import sqlite3
# from flask import Flask, g, jsonify, request, url_for
# from math import ceil

# def dict_factory(cursor, row):
#  """Arma un diccionario con los valores de la fila."""
#  fields = [column[0] for column in cursor.description]
#  return {key: value for key, value in zip(fields, row)}

# def abrirConexion():
#   if 'db' not in g:
#      g.db = sqlite3.connect("SQL_Sensor.sqlite")
#      g.db.row_factory = dict_factory
#   return g.db


# def cerrarConexion(e=None):
#    db = g.pop('db', None)
#    if db is not None:
#        db.close()


# app = Flask(__name__)
# app.teardown_appcontext(cerrarConexion)
# resultados_por_pag = 10

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"


# @app.route("/api/sensor",methods=["POST"])
# def sensor():
#     abrirConexion()

#     datos = request.json
#     nombre = datos["nombre"]
#     valor = datos["valor"]

#     print (f"sensor: {nombre}, valor: {valor}")
#     cerrarConexion()

#     return "OK"
