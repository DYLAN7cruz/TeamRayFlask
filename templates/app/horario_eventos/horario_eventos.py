from flask import Flask, jsonify, render_template, url_for, request, redirect, flash, session
import flask
import psycopg2
import psycopg2.extras
import re

from database.base import get_conection
conn = get_conection()


horario_evento = flask.Blueprint('horario_evento', __name__)

#--------------------------------HORARIO EVENTO--------------------------------------------


@horario_evento.route('/templates/app/horario_eventos/nuevo_horario_eventos.html')
def nuevo_horario_evento():
    if 'loggedin' in session:

        return render_template('app/horario_eventos/nuevo_horario_eventos.html')
    
    flash('Debes iniciar sesión para acceder a esta página.')

    return render_template('web/loginn.html')

#------------------------------ AQUI AGREGA EL HORARIO EVENTO EL ESTUDIANTE-------------------------------

@horario_evento.route('/add_horario_eventos', methods=['GET', 'POST'])
def add_horario_eventos():
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
        if request.method == 'POST':
        
           hora_inicio = request.form['hora_inicio']
           hora_fin = request.form['hora_fin']
           dia = request.form['dia']
        

           cur.execute("INSERT INTO horarios.horario_eventos (hora_inicio, hora_fin, dia) VALUES (%s, %s, %s)",
                    ( hora_inicio, hora_fin, dia))
        
           conn.commit()
           flash('¡Registro realizada con éxito!')
        return redirect(url_for('horario_evento.nuevo_horario_evento'))
    

    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')



#----------------------- ver nuevo horario eventos ------------------------------

@horario_evento.route('/templates/app/horario_eventos/horario_eventos.html', methods=['POST', 'GET'])
def horario_eventos():
    # Comprobar si el usuario ha iniciado sesión
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if request.method == "POST" and 'buscar' in request.form and request.form['buscar'].strip():
            search_term = "%" + request.form['buscar'].strip() + "%"
            
            # Consulta para buscar por día
            s = """
                SELECT * 
                FROM horarios.horario_eventos
                WHERE dia ILIKE %s
                ORDER BY id ASC
            """
            cur.execute(s, (search_term,))
            
        else:
            s = "SELECT id, TO_CHAR(hora_inicio, 'HH12:MI AM') AS hora_inicio, TO_CHAR(hora_fin, 'HH12:MI AM') AS hora_fin, dia FROM horarios.horario_eventos ORDER BY id ASC "
            cur.execute(s)
        list_horario_eventos = cur.fetchall()

        return render_template('app/horario_eventos/horario_eventos.html', list_horario_eventos=list_horario_eventos)

    # El usuario no ha iniciado sesión redirigir a la página de inicio de sesión
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')

#-------------------ACTUALIZA LOS HORARIO_EVENTOS-------------------------


@horario_evento.route('/edit_horario_evento/<id>', methods=['POST', 'GET'])
def get_comentario(id):
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute('SELECT * FROM horarios.horario_eventos WHERE id = %s', (id,))
        data = cur.fetchall()
        cur.close()
        print(data[0])
        return render_template('app/horario_eventos/editar_horario_eventos.html', horario_evento=data[0])
    
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')


#-------------------ACTUALIZA EL HORRARIO_EVENTO HECHO POR EL ESTUDIANTES-----------------------------


@horario_evento.route('/update_horario_evento/<id>', methods=['POST'])
def update_horario_evento(id):
    if 'loggedin' in session:
        if request.method == 'POST':
            hora_inicio = request.form['hora_inicio']
            hora_fin = request.form['hora_fin']
            dia = request.form['dia']
            

            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("""
              UPDATE horarios.horario_eventos
              SET hora_inicio = %s,
                        hora_fin = %s,
                        dia= %s
                        
                  
                  
              WHERE id             = %s
          """, (hora_inicio, hora_fin, dia, id))
            flash('Cambios guardados con éxito')
            conn.commit()
            return redirect(url_for('horario_evento.horario_eventos'))
        
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')
    
#-----------------------ELIMINAR HORARIO_EVENTOS-----------------------

@horario_evento.route('/deletehorario_eventos/<string:id>', methods=['POST', 'GET'])
def delete_horario_eventos(id):
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
                DELETE FROM horarios.horario_eventos WHERE id = %s
                """, (id,))
        conn.commit()
        flash('Horario evento Eliminado Correctamente')
        return redirect(url_for('horario_evento.horario_eventos'))
    
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')