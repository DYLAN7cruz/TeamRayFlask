from flask import Flask, jsonify, render_template, url_for, request, redirect, flash, session
import flask
import psycopg2
import psycopg2.extras
import re

from database.base import get_conection
conn = get_conection()


modalidad = flask.Blueprint('modalidad', __name__)

#--------------------------------HORARIO EVENTO--------------------------------------------


@modalidad.route('/templates/app/modalidad/nueva_modalidad.html')
def nueva_modalidad():
    if 'loggedin' in session:

        return render_template('app/modalidad/nueva_modalidad.html')
    
    flash('Debes iniciar sesión para acceder a esta página.')

    return render_template('web/loginn.html')

#------------------------------ AQUI AGREGA MODALIDAD -------------------------------

@modalidad.route('/add_modalidad', methods=['GET', 'POST'])
def add_modalidad():
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
        if request.method == 'POST':
           nombre = request.form['nombre']

           cur.execute("INSERT INTO eventos.modalidad (nombre) VALUES (%s)",
                    (nombre,))
        
           conn.commit()
           flash('¡Registro realizada con éxito!')
        return redirect(url_for('modalidad.modalidadd'))
    
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')

#----------------------- ver nuevA MODALIDAD ------------------------------

@modalidad.route('/templates/app/modalidad/modalidad.html', methods=['POST', 'GET'])
def modalidadd():
    # Comprobar si el usuario ha iniciado sesión
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if request.method == "POST" and 'buscar' in request.form and request.form['buscar'].strip():
            search_term = "%" + request.form['buscar'].strip() + "%"
            
            # Consulta para buscar por día
            s = """
                SELECT * 
                FROM eventos.modalidad
                WHERE nombre ILIKE %s
                ORDER BY id ASC
            """
            cur.execute(s, (search_term,))
            
        else:
            s = "SELECT * FROM eventos.modalidad ORDER BY id ASC "
            cur.execute(s)
        list_modalidad = cur.fetchall()

        return render_template('app/modalidad/modalidad.html', list_modalidad=list_modalidad)

    # El usuario no ha iniciado sesión redirigir a la página de inicio de sesión
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')

#-------------------ACTUALIZA LO MODALIDAD-------------------------


@modalidad.route('/edit_modalidad/<id>', methods=['POST', 'GET'])
def get_modalidado(id):
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute('SELECT * FROM eventos.modalidad WHERE id = %s', (id,))
        data = cur.fetchall()
        cur.close()
        print(data[0])
        return render_template('app/modalidad/editar_modalidad.html', modalidad=data[0])
    
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')


#-------------------ACTUALIZA LA MODALIDAD-----------------------------


@modalidad.route('/update_modalidad/<id>', methods=['POST'])
def update_modalidad(id):
    if 'loggedin' in session:
        if request.method == 'POST':
            nombre = request.form['nombre']

            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("""
              UPDATE eventos.modalidad
              SET nombre = %s
                  
              WHERE id             = %s
          """, (nombre, id))
            flash('Cambios guardados con éxito')
            conn.commit()
            return redirect(url_for('modalidad.modalidadd'))
        
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')

#-----------------------ELIMINAR MODALIDAD-----------------------

@modalidad.route('/deletemodalidad/<string:id>', methods=['POST', 'GET'])
def delete_modalidad(id):
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
                DELETE FROM eventos.modalidad WHERE id = %s
                """, (id,))
        conn.commit()
        flash('Modalidad Eliminada Correctamente')
        return redirect(url_for('modalidad.modalidadd'))
    
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')