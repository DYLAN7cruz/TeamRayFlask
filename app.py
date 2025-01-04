from flask import Flask, jsonify, render_template, url_for, request, redirect, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
#---------------BLUEPRINTS DE LA WEB-------------------
from templates.web.web import web
#---------------BLUEPRINTS DE LOS CRUDS PERSONAL-------------------
from templates.app.personal.personal import personal
#----------------BLUEPRINT DE LOS COMENTARIOS------------
from templates.app.comentarios.comentarios import comentarios 
#----------------BLUEPRINT DE LAS NOTIFICACIONES------------
from templates.app.notificaciones.notificaciones import notificaciones 
#----------------BLUEPRINT DE EL ADMINISTRADOR------------
from templates.app.conector import administrador
#----------------BLUEPRINT DE EL ADMINISTRADOR------------
from templates.app.matriculas.matricula import matricula

import psycopg2
import psycopg2.extras
import re
# Traer la conexion
from database.base import get_conection
conn = get_conection()

app = Flask(__name__, static_url_path='/static')
app.secret_key = "capuli"

#---------------------TRAEMOS LA INFORMACION DE EL WEB.PY----------------------
app.register_blueprint(web)

#--------------------TRAEMAS LA INFORMACION SOBRE EL CRUD DEL PERSONAL-------------------------------
app.register_blueprint(personal)

#--------------------TRAEMAS LA INFORMACION SOBRE TODOS LOS CRUDS DE LOS COMETARIOS-------------------------------
app.register_blueprint(comentarios)

#--------------------TRAEMAS LA INFORMACION SOBRE TODOS LOS CRUDS DE LAS NOTIFICACIONES-------------------------------
app.register_blueprint(notificaciones)

#--------------------TRAEMAS LA INFORMACION SOBRE EL ADMIN-------------------------------
app.register_blueprint(administrador)

#--------------------TRAEMAS LA INFORMACION SOBRE LA MATRICULA-------------------------------
app.register_blueprint(matricula)




# cerrar sesion
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('nombre_rol', None)
    session.pop('nombres', None)
    session.pop('apellidos', None)
    session.pop('fecha_nacimiento', None)
    session.pop('fecha_inscripcion', None)
    session.pop('nombre_cinturon', None)
    session.pop('genero', None)
    session.pop('correo', None)
    session.clear()
    # Redirect to login page
    return render_template('web/loginn.html')


if __name__ == '__main__':
    app.run(debug=True)