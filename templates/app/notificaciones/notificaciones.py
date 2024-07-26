from flask import Flask, jsonify, render_template, url_for, request, redirect, flash, session
import flask
import psycopg2
import psycopg2.extras
import re

from database.base import get_conection
conn = get_conection()


notificaciones = flask.Blueprint('notificaciones', __name__)


#--------------------HACER NOTIFICACIONES-----------------------------


@notificaciones.route('/templates/app/notificaciones/nueva_notificacion.html')
def nueva_notificacion():
    if 'loggedin' in session:
        return render_template('app/notificaciones/nueva_notificacion.html')
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')

#------------------------------ AQUI AGREGA LA NOTIFICACION EL ENTRENADOR-------------------------------

@notificaciones.route('/add_notificacion', methods=['GET', 'POST'])
def add_notificacion():
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
        if request.method == 'POST':
        
            descripcion = request.form['descripcion']
            id_personas = request.form['persona']
        

            cur.execute("INSERT INTO personas.notificaciones (descripcion,id_personas) VALUES (%s, %s)",
                    ( descripcion, id_personas))
        
            conn.commit()
            flash('¡Notificacion realizada con éxito!')

            
        return redirect(url_for('notificaciones.notificacioness'))
    
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')

#-----------------VER LAS NOTOFICACIONES----------------

@notificaciones.route('/templates/app/notificaciones/notificaciones.html', methods=['POST', 'GET'])
def notificacioness():
    

    # Comprobar si el usuario ha iniciado sesión
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if request.method == "POST" and 'buscar' in request.form:
            search_term = "%" + request.form['buscar'] + "%"
            s = "SELECT * FROM personas.notificaciones WHERE descripcion LIKE %s;"
            cur.execute(s, (search_term,))
            
        else:
            s = "select * from personas.notificaciones"
            cur.execute(s)  # Ejecutar la instrucción SQL

        list_notificacion = cur.fetchall()

        return render_template('app/notificaciones/notificaciones.html', list_notificacion=list_notificacion)

    # El usuario no ha iniciado sesión redirigir a la página de inicio de sesión
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')


#---------------------EDITAR LAS NOTIFICACIONES-------------------

@notificaciones.route('/editnotificacion/<id>', methods=['POST', 'GET'])
def get_notificacion(id):
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute('SELECT * FROM personas.notificaciones WHERE id = %s', (id,))
        data = cur.fetchall()
        cur.close()
        print(data[0])
        return render_template('app/notificaciones/editar_notificacion.html', notificacion=data[0])
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')


#-------------------ACTUALIZA EN LA BASE LAS NOTOFICACIONES-----------------------------


@notificaciones.route('/update_notificacion/<id>', methods=['POST'])
def update_notificacion(id):
    if 'loggedin' in session:
        if request.method == 'POST':
            descripcion = request.form['descripcion']
            
            

            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("""
              UPDATE personas.notificaciones
              SET descripcion         = %s
                  
                  
              WHERE id             = %s
          """, (descripcion, id))
            flash('Cambios guardados con éxito')
            conn.commit()
            return redirect(url_for('notificaciones.notificacioness'))

    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')

#-----------------------ELIMINAR NOTIFICACIONES-----------------------

@notificaciones.route('/deletenotificacion/<string:id>', methods=['POST', 'GET'])
def delete_notificacion(id):
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
                DELETE FROM personas.notificaciones WHERE id = %s
                """, (id,))
        conn.commit()
        flash('Notificacion Eliminada Correctamente')
        return redirect(url_for('notificaciones.notificacioness'))
    
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')


#---------------------MOSTRAR NOTIFICACIONES--------------------------------


@notificaciones.route('/templates/app/notificaciones/ver_notificaciones.html', methods=['POST', 'GET'])
def mis_notificaciones():
    if 'loggedin' in session:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Obtener el número de notificaciones
        cursor.execute("SELECT COUNT(*) FROM personas.notificaciones")
        count = cursor.fetchone()[0]

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if request.method == "POST" and 'buscar' in request.form:
            search_term = "%" + request.form['buscar'] + "%"
            s = "SELECT descripcion FROM personas.notificaciones WHERE descripcion LIKE %s"
            cur.execute(s, (search_term,))
            

        else:
            s = "SELECT descripcion FROM personas.notificaciones"
            cur.execute(s)

        notificaciones = cur.fetchall()

        return render_template('app/notificaciones/ver_notificaciones.html', count=count, notificaciones=notificaciones)
    
    # El usuario no ha iniciado sesión, redirigir a la página de inicio de sesión
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')



@notificaciones.route('/templates/app/menus/menuestudiante.html', methods=['GET'])
def menuestudiante():
    if 'loggedin' in session:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Obtener el número de notificaciones
        cursor.execute("SELECT COUNT(*) FROM personas.notificaciones")
        count = cursor.fetchone()[0]

        return render_template('app/menus/menuestudiante.html', count=count)

    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')