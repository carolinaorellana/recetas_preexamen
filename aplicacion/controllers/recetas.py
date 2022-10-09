
from aplicacion import app
from flask import render_template, redirect, request, session, flash
from aplicacion.models.receta import Receta

#ruta para renderizar la pagina de nueva receta
@app.route('/nueva_receta')
def nueva_receta():
    if session['login']==True:
        return render_template("nueva_receta.html")
    else:
        return redirect ('/') 

#ruta para crear una receta en la base de datos
@app.route ('/crear_receta', methods=['POST'])
def crear_receta():
    if not Receta.validacion_receta(request.form):
        return redirect("/nueva_receta")
    data={
        "titulo": request.form['titulo'],
        "descripcion": request.form['descripcion'],
        "instrucciones": request.form['instrucciones'],
        "fecha": request.form['fecha'],
        "duracion": request.form['duracion'],
        "usuario_id": request.form['usuario_id'],
    }
    receta_id=Receta.crear_receta(data)
    # print(receta_id)
    #este hay que cambiarlo a que se redirect la receta creada solamente.
    return redirect(f"/receta/{receta_id}")

#ruta para mostrar la info de una receta
@app.route('/receta/<int:id>')
def leer_receta(id):
    if session['login']==True:
        data={
            "id": id
        }
        una_receta=Receta.leer_receta(data)
        # print(una_receta)
        return render_template('leer_receta.html',una_receta=una_receta)
    else:
        return redirect ('/') 

#ruta para mostrar la pantalla que edita la receta
@app.route('/receta/<int:id>/editar')
def permite_editar_receta(id):
    if session['login']==True:
        data={
            "id": id
        }
        una_receta=Receta.leer_receta(data)
        return render_template ("editar_receta.html", una_receta= una_receta)
    else:
        return redirect ('/') 

#ruta para editar una receta
@app.route("/editar_receta",  methods=['POST'])
def editar_receta():
    if not Receta.validacion_receta(request.form):
        return redirect(f"/receta/{request.form['id']}/editar")
    data={
            "id":request.form['id'],
            "titulo": request.form['titulo'],
            "descripcion": request.form['descripcion'],
            "instrucciones": request.form['instrucciones'],
            "fecha": request.form['fecha'],
            "duracion": request.form['duracion'],
        }
    editar_una_receta = Receta.editar_receta(data)
    # print (editar_una_receta)
    return redirect (f"/receta/{request.form['id']}")

#ruta para eliminar receta
@app.route("/receta/<int:id>/eliminar")
def eliminar_receta(id):
    data={
        "id":id
    }
    Receta.eliminar_receta(data)
    return redirect(f"bienvenido/{session['usuario_id']}")