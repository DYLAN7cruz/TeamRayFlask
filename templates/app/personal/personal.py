
from flask import Flask, get_flashed_messages, jsonify, render_template, url_for, request, redirect, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import flask
import psycopg2
import psycopg2.extras
import re

from database.base import get_conection
conn = get_conection()

personal = flask.Blueprint('personal', __name__)

@personal.route('/templates/app/personal/nueva_persona.html')
def nueva_persona():
    if 'loggedin' in session:
       return render_template('app/personal/nueva_persona.html')
    # El usuario no ha iniciado sesión, redirigir a la página de inicio de sesión
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')


@personal.route('/agregar_empleado', methods=['GET', 'POST'])
def agregar_empleado():
    if 'loggedin' in session:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if request.method == 'POST' and 'id' in request.form and 'clave' in request.form:
            id = request.form['id']
            nombres = request.form['nombres']
            apellidos = request.form['apellidos']
            fecha_nacimiento = request.form['fecha_nacimiento']
            fecha_inscripcion = request.form['fecha_inscripcion']
            clave = request.form['clave']
            nombre_cinturon = request.form['nombre_cinturon']
            genero = request.form['genero']
            nombre_rol = request.form['nombre_rol']
            correo = request.form['correo']
            telefono = request.form['telefono']
            direccion = request.form['direccion']

            if not re.match(r'[^@]+@[^@]+\.[^@]+', correo):
                flash('¡Dirección de correo electrónico no válida!')
            elif not re.match(r'[A-Za-z0-9]+', nombres):
                flash('¡El nombre de usuario debe contener solo caracteres y números!')
            elif not nombres or not correo or not clave:
                flash('¡Por favor rellena el formulario!')
            else:
                cursor.execute('SELECT * FROM personas.personas WHERE id = %s', (id,))
                account = cursor.fetchone()

                if account:
                    flash('La cuenta que ingresaste ya existe')
                else:
                    hashed_password = generate_password_hash(clave)
                    cursor.execute("""
                        INSERT INTO personas.personas (id, nombres, apellidos, fecha_nacimiento, fecha_inscripcion, clave, nombre_cinturon, genero, nombre_rol, correo,telefono,direccion)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (id, nombres, apellidos, fecha_nacimiento, fecha_inscripcion, hashed_password, nombre_cinturon, genero, nombre_rol, correo,telefono, direccion))
                    conn.commit()
                    flash('¡Usuario registrado correctamente!')
                return redirect(url_for('personal.usuario'))
            return redirect(url_for('personal.usuario'))

        return render_template('app/personal/persona.html')
    # El usuario no ha iniciado sesión, redirigir a la página de inicio de sesión

    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')


@personal.route('/templates/app/personal/persona.html', methods=['POST', 'GET'])
def usuario():
    if 'loggedin' in session:
        
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            if request.method == "POST" and 'buscar' in request.form:
                s = "SELECT * FROM personas.personas WHERE id LIKE '%" + request.form['buscar'] + "%'"
            else:
                s = "SELECT * FROM personas.personas"
            cur.execute(s)
            list_users = cur.fetchall()
            return render_template('app/personal/persona.html', list_users=list_users)
    
    flash('Debes iniciar sesión para acceder a esta página.')     
    return render_template('web/loginn.html')


@personal.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_empleados(id):
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("DELETE FROM personas.personas WHERE id = %s", (id,))
        conn.commit()
        
        flash('Usuario eliminado correctamente')
        return redirect(url_for('personal.usuario'))

    flash('Debes iniciar sesión para acceder a esta página.')
    return redirect(url_for('personal.usuario'))


@personal.route('/edit/<id>', methods=['POST', 'GET'])
def get_empleado(id):
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute('SELECT * FROM personas.personas WHERE id = %s', (id,))
        data = cur.fetchall()
        cur.close()

        
        return render_template('app/personal/editar_persona.html', personas=data[0])
    
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')


@personal.route('/update_persona/<id>', methods=['POST'])
def update(id):
    if 'loggedin' in session:
        if request.method == 'POST':
            nombres = request.form['nombres']
            apellidos = request.form['apellidos']
            fecha_nacimiento = request.form['fecha_nacimiento']
            fecha_inscripcion = request.form['fecha_inscripcion']
            clave = request.form['clave']
            nombre_cinturon = request.form['nombre_cinturon']
            genero = request.form['genero']
            nombre_rol = request.form['nombre_rol']
            correo = request.form['correo']

            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            # Verificar si se ingresó una nueva contraseña
            if clave:
                hashed_password = generate_password_hash(clave)
                cur.execute("""
                    UPDATE personas.personas
                    SET nombres = %s,
                        apellidos = %s,
                        fecha_nacimiento = %s,
                        fecha_inscripcion = %s,
                        clave = %s,
                        nombre_cinturon = %s,
                        genero = %s,
                        nombre_rol = %s,
                        correo = %s
                    WHERE id = %s
                """, (nombres, apellidos, fecha_nacimiento, fecha_inscripcion, hashed_password, nombre_cinturon, genero, nombre_rol, correo, id))
            else:
                cur.execute("""
                    UPDATE personas.personas
                    SET nombres = %s,
                        apellidos = %s,
                        fecha_nacimiento = %s,
                        fecha_inscripcion = %s,
                        nombre_cinturon = %s,
                        genero = %s,
                        nombre_rol = %s,
                        correo = %s
                    WHERE id = %s
                """, (nombres, apellidos, fecha_nacimiento, fecha_inscripcion, nombre_cinturon, genero, nombre_rol, correo, id))
                
            flash('Cambios guardados con éxito')
            conn.commit()
            return redirect(url_for('personal.usuario'))
        
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')