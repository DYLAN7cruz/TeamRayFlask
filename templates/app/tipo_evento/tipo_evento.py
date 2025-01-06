from flask import Flask, jsonify, render_template, url_for, request, redirect, flash, session
import flask
import psycopg2
import psycopg2.extras
import re

from database.base import get_conection
conn = get_conection()


tipo_evento = flask.Blueprint('tipo_evento', __name__)

#--------------------------------HORARIO EVENTO--------------------------------------------


@tipo_evento.route('/templates/app/tipo_evento/nuevo_tipo_evento.html')
def nuevo_tipo_evento():
    if 'loggedin' in session:

        return render_template('app/tipo_evento/nuevo_tipo_evento.html')
    
    flash('Debes iniciar sesión para acceder a esta página.')

    return render_template('web/loginn.html')

#------------------------------ AQUI AGREGA EL TIPO EVENTO -------------------------------

@tipo_evento.route('/add_tipo_eventos', methods=['GET', 'POST'])
def add_tipo_eventos():
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
        if request.method == 'POST':
           nombre = request.form['nombre']

           cur.execute("INSERT INTO eventos.tipo_evento (nombre) VALUES (%s)",
                    (nombre,))
        
           conn.commit()
           flash('¡Registro realizada con éxito!')
        return redirect(url_for('tipo_evento.tipo_eventoo'))
    
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')

#----------------------- ver nuevo TIPO eventos ------------------------------

@tipo_evento.route('/templates/app/tipo_evento/tipo_evento.html', methods=['POST', 'GET'])
def tipo_eventoo():
    # Comprobar si el usuario ha iniciado sesión
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if request.method == "POST" and 'buscar' in request.form and request.form['buscar'].strip():
            search_term = "%" + request.form['buscar'].strip() + "%"
            
            # Consulta para buscar por día
            s = """
                SELECT * 
                FROM eventos.tipo_evento
                WHERE nombre ILIKE %s
                ORDER BY id ASC
            """
            cur.execute(s, (search_term,))
            
        else:
            s = "SELECT * FROM eventos.tipo_evento ORDER BY id ASC "
            cur.execute(s)
        list_tipo_eventos = cur.fetchall()

        return render_template('app/tipo_evento/tipo_evento.html', list_tipo_eventos=list_tipo_eventos)

    # El usuario no ha iniciado sesión redirigir a la página de inicio de sesión
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')

#-------------------ACTUALIZA LOS TIPO_EVENTOS-------------------------


@tipo_evento.route('/edit_tipo_evento/<id>', methods=['POST', 'GET'])
def get_tipo_evento(id):
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute('SELECT * FROM eventos.tipo_evento WHERE id = %s', (id,))
        data = cur.fetchall()
        cur.close()
        print(data[0])
        return render_template('app/tipo_evento/editar_tipo_evento.html', tipo_evento=data[0])
    
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')


#-------------------ACTUALIZA EL TIPO_EVENTO-----------------------------


@tipo_evento.route('/update_tipo_evento/<id>', methods=['POST'])
def update_tipo_evento(id):
    if 'loggedin' in session:
        if request.method == 'POST':
            nombre = request.form['nombre']

            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("""
              UPDATE eventos.tipo_evento
              SET nombre = %s
                  
              WHERE id             = %s
          """, (nombre, id))
            flash('Cambios guardados con éxito')
            conn.commit()
            return redirect(url_for('tipo_evento.tipo_eventoo'))
        
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')

#-----------------------ELIMINAR TIPO_EVENTOS-----------------------

@tipo_evento.route('/deletetipo_eventos/<string:id>', methods=['POST', 'GET'])
def delete_tipo_eventos(id):
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
                DELETE FROM eventos.tipo_evento WHERE id = %s
                """, (id,))
        conn.commit()
        flash('Tipo evento Eliminado Correctamente')
        return redirect(url_for('tipo_evento.tipo_eventoo'))
    
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')