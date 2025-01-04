
from flask import Flask, jsonify, render_template, url_for, request, redirect, flash, session
import flask
import psycopg2
import psycopg2.extras
import re

from database.base import get_conection
conn = get_conection()


comentarios = flask.Blueprint('comentarios', __name__)

#--------------------------------COMENTARIO DEL ESTUDIANTE--------------------------------------------


@comentarios.route('/templates/app/comentarios/nuevo_comentario.html')
def nuevo_comentario():
    if 'loggedin' in session:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute("SELECT COUNT(*) FROM personas.notificaciones")
        count = cursor.fetchone()[0]

        return render_template('app/comentarios/nuevo_comentario.html', count=count)
    
    flash('Debes iniciar sesión para acceder a esta página.')

    return render_template('web/loginn.html')

#------------------------------ AQUI AGREGA EL COMENTARIO EL ESTUDIANTE-------------------------------

@comentarios.route('/add_comentario', methods=['GET', 'POST'])
def add_comentario():
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
        if request.method == 'POST':
        
           descripcion = request.form['descripcion']
           id_personas = request.form['persona']
        

           cur.execute("INSERT INTO personas.comentarios (descripcion,id_personas) VALUES (%s, %s)",
                    ( descripcion, id_personas))
        
           conn.commit()
           flash('¡Comentario realizada con éxito!')
        return redirect(url_for('comentarios.comentario3'))
    

    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')


#--------------------------- AQUI SE MUESTRAN LOS COMETARIOS EN EL ADMIN, MUESTRA LOS COMENTARIO DE TODOS LOS ESTUDIANTES------------------------

@comentarios.route('/templates/app/comentarios/comentario.html', methods=['POST', 'GET'])
def comentario():
    # Comprobar si el usuario ha iniciado sesión
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if request.method == "POST" and 'buscar' in request.form:
            search_term = "%" + request.form['buscar'] + "%"
            s = "SELECT personas.comentarios.*, personas.nombres, personas.apellidos FROM personas.comentarios JOIN personas.personas ON comentarios.id_personas = personas.id WHERE descripcion LIKE %s;"
            cur.execute(s, (search_term,))
            
        else:
            s = "SELECT personas.comentarios.*, personas.nombres, personas.apellidos FROM personas.comentarios JOIN personas.personas ON comentarios.id_personas = personas.id;"
            cur.execute(s)
        list_comentarios = cur.fetchall()

        return render_template('app/comentarios/comentario.html', list_comentarios=list_comentarios)

    # El usuario no ha iniciado sesión redirigir a la página de inicio de sesión
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')
    
    





#-------------------------------AQUI SOLO SE MUESTRA EL COMENTARIO DE LA PERSONA QUE INGRESA A SU SESSION------------------------------



@comentarios.route('/templates/app/comentarios/comentario3.html', methods=['POST', 'GET'])
def comentario3():
    # Comprobar si el usuario ha iniciado sesión
    if 'loggedin' in session:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute("SELECT COUNT(*) FROM personas.notificaciones")
        count = cursor.fetchone()[0]

    
    
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if request.method == "POST" and 'buscar' in request.form:
           search_term = "%" + request.form['buscar'] + "%"
           s = "SELECT descripcion FROM personas.comentarios WHERE id_personas = %s AND descripcion LIKE %s"
           cur.execute(s, (session['id'], search_term))
        else:
           s = "select comentarios.descripcion from personas.comentarios where comentarios.id_personas = '" + session['id'] + "'"
           cur.execute(s, (session['id'],))

        list_comentarios = cur.fetchall()
        return render_template('app/comentarios/comentario3.html', list_comentarios=list_comentarios, count=count)

    # El usuario no ha iniciado sesión, redirigir a la página de inicio de sesión
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')









@comentarios.route('/delete_comentario/<string:id>', methods=['POST', 'GET'])
def delete_comentario(id):
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
                DELETE FROM personas.comentarios WHERE id = %s
                """, (id,))
        conn.commit()
        flash('Comentario Eliminado Correctamente') 
        return redirect(url_for('comentarios.comentario'))
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')
    

#------------------------------ELIMINA LOS COMENTARIOS

@comentarios.route('/delete_comentario3/<string:descripcion>', methods=['POST', 'GET'])
def delete_comentario3(descripcion):
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
                DELETE FROM personas.comentarios WHERE descripcion = %s
                """, (descripcion,))
        conn.commit()
        flash('Comentario Eliminado Correctamente')
        return redirect(url_for('comentarios.comentario3'))
    
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')

#-------------------ACTUALIZA LOS COMENTARIOS-------------------------


@comentarios.route('/edit_comentario/<id>', methods=['POST', 'GET'])
def get_comentario(id):
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute('SELECT * FROM personas.comentarios WHERE descripcion = %s', (id,))
        data = cur.fetchall()
        cur.close()
        print(data[0])
        return render_template('app/comentarios/editar_comentarios.html', comentarios=data[0])
    
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')


#-------------------ACTUALIZA EL COMENTARIO HECHO POR EL ESTUDIANTES-----------------------------


@comentarios.route('/update_comentario/<id>', methods=['POST'])
def update_comentario(id):
    if 'loggedin' in session:
        if request.method == 'POST':
            descripcion = request.form['descripcion']
            
            

            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("""
              UPDATE personas.comentarios
              SET descripcion         = %s
                  
                  
              WHERE id             = %s
          """, (descripcion, id))
            flash('Cambios guardados con éxito')
            conn.commit()
            return redirect(url_for('comentarios.comentario3'))
        
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')