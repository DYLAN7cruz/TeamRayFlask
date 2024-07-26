
from flask import Flask, jsonify, render_template, url_for, request, redirect, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import flask
import psycopg2
import psycopg2.extras
import re

from database.base import get_conection
conn = get_conection()

web = flask.Blueprint('web', __name__)


@web.route('/login/', methods=['GET', 'POST'])
def login():

    
    
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute("SELECT COUNT(*) FROM personas.notificaciones")
    count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM personas.personas WHERE nombre_rol = 'Estudiante' ")
    countt = cursor.fetchone()[0]

    if request.method == 'POST' and 'id' in request.form and 'clave' in request.form:
        id = request.form['id']
        clave = request.form['clave']

        cursor.execute('SELECT * FROM personas.personas WHERE id = %s', (id,))
        account = cursor.fetchone()

        if account:
            password_rs = account['clave']
            if check_password_hash(password_rs, clave):
                session['loggedin'] = True
                session['id'] = account['id']
                session['nombre_rol'] = account['nombre_rol']
                session['nombres'] = account['nombres']
                session['apellidos'] = account['apellidos']
                session['fecha_nacimiento'] = account['fecha_nacimiento']
                session['fecha_inscripcion'] = account['fecha_inscripcion']
                session['nombre_cinturon'] = account['nombre_cinturon']
                session['genero'] = account['genero']
                
                session['correo'] = account['correo']
                session['telefono'] = account['telefono']
                session['direccion'] = account['direccion']

                if session['nombre_rol'] == "Administrador":
                    return render_template('app/admin.html',countt=countt)
                elif session['nombre_rol'] == "Entrenador":
                    return render_template('app/entrenador.html')
                elif session['nombre_rol'] == "Estudiante":
                    return render_template('app/estudiante.html', count=count)
            else:
                flash('Nombre de usuario/contraseña incorrectos')
        else:
            flash('Nombre de usuario/contraseña incorrectos')

    return render_template('web/loginn.html')



    # Obtener el número de notificaciones
    
#----------------------TEMPLATES/WEB---------------------------------

#---------------------------INDEX.HTML--------------------------------
@web.route('/')
def index():
    return render_template('web/index.html')


#---------------------------SERVICIOS.HTML--------------------------
@web.route('/templates/web/servicios.html')
def servicios():
    return render_template('web/servicios.html')


#---------------------------EVENTOS.HTML--------------------------
@web.route('/templates/web/eventos.html')
def eventos():
    return render_template('web/eventos.html')


#---------------------------CONTACTANOS.HTML--------------------------
@web.route('/templates/web/contactanos.html')
def contactanos():
    return render_template('web/contactanos.html')


#---------------------------LOGIN.HTML--------------------------
@web.route('/templates/web/loginn.html')
def loginn():
    return render_template('web/loginn.html')





#---------------------------COMETARIOS.HTML--------------------------
@web.route('/templates/web/comentario2.html', methods=['POST', 'GET'] )
def comentario2():
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if request.method == "POST" and 'buscar' in request.form:
            s = "select personas.comentarios. * , personas.nombres from personas.comentarios join personas.personas on comentarios.id_personas= '" + \
                request.form['buscar'] + "'"
        else:
            s = "select personas.comentarios. * , personas.nombres, personas.apellidos from personas.comentarios join personas.personas on comentarios.id_personas= personas.id;"
        cur.execute(s)  # Ejecutar la instrucción SQL
        list_comentarios = cur.fetchall()
        return render_template('web/comentario2.html', list_comentarios=list_comentarios)



