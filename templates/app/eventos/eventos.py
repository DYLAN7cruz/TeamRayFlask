from flask import Flask, jsonify, render_template, url_for, request, redirect, flash, session
import flask
import psycopg2
import psycopg2.extras
import re

from database.base import get_conection
conn = get_conection()


eventos = flask.Blueprint('eventos', __name__)

#--------------------------------HORARIO EVENTO--------------------------------------------


@eventos.route('/templates/app/eventos/nuevo_evento.html')
def nuevo_evento():
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Obtener la lista de horarios disponibles
        cur.execute("SELECT id, TO_CHAR(hora_inicio, 'HH12:MI AM') AS hora_inicio, TO_CHAR(hora_fin, 'HH12:MI AM') AS hora_fin, dia FROM horarios.horario_eventos")
        horarios = cur.fetchall()

        cur.execute("SELECT id, nombre FROM eventos.tipo_evento")
        tipo_evento = cur.fetchall()

        return render_template('app/eventos/nuevo_evento.html', horarios=horarios, tipo_evento=tipo_evento)
    
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')

#------------------------------ AQUI AGREGA EVENTOS -------------------------------

@eventos.route('/add_eventos', methods=['GET', 'POST'])
def add_eventos():
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
        if request.method == 'POST':
            nombre = request.form['nombre']
            id_horario_evento = request.form['id_horario_evento']
            direccion = request.form['direccion']
            id_tipo_evento = request.form['id_tipo_evento']
            fecha = request.form['fecha']
    
            cur.execute("""
                INSERT INTO eventos.eventos (nombre, id_horario_eventos, direccion, id_tipo_evento, fecha) 
                VALUES (%s, %s, %s, %s, %s)
            """, (nombre, id_horario_evento, direccion, id_tipo_evento, fecha))
                
            conn.commit()
            flash('¡Registro realizado con éxito!')
            
            
        return redirect(url_for('eventos.ver_eventos'))
    
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')

#----------------------- VER EVENTOS ------------------------------

@eventos.route('/templates/app/eventos/eventos.html', methods=['POST', 'GET'])
def ver_eventos():
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if request.method == "POST" and 'buscar' in request.form and request.form['buscar'].strip():
            search_term = "%" + request.form['buscar'].strip() + "%"

            # Consulta con búsqueda por nombre de evento
            s = """
                SELECT e.id, e.nombre, e.direccion, e.fecha, 
                       CONCAT(h.dia, ' - ', h.hora_inicio, ' a ', h.hora_fin) AS horario_evento,
                       t.nombre AS tipo_evento
                FROM eventos.eventos e
                JOIN horarios.horario_eventos h ON e.id_horario_eventos = h.id
                JOIN eventos.tipo_evento t ON e.id_tipo_evento = t.id
                WHERE e.nombre ILIKE %s
                ORDER BY e.id ASC
            """
            cur.execute(s, (search_term,))
        else:
            # Consulta para mostrar todos los eventos
            s = """
                SELECT e.id, e.nombre, e.direccion, e.fecha, 
                       CONCAT(h.dia, ' - ', TO_CHAR(h.hora_inicio, 'HH12:MI AM'),' a ', TO_CHAR(h.hora_fin, 'HH12:MI AM')) AS horario_evento,
                       t.nombre AS tipo_evento
                FROM eventos.eventos e
                JOIN horarios.horario_eventos h ON e.id_horario_eventos = h.id
                JOIN eventos.tipo_evento t ON e.id_tipo_evento = t.id
                ORDER BY e.id ASC
            """
            cur.execute(s)
        
        list_eventos = cur.fetchall()

        return render_template('app/eventos/eventos.html', list_eventos=list_eventos)

    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')

#-------------------ACTUALIZA EL EVENTO-------------------------


@eventos.route('/edit_evento/<id>', methods=['POST', 'GET'])
def get_evento(id):
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Obtener el evento específico
        cur.execute("""
            SELECT e.id, e.nombre, e.direccion, e.fecha, e.id_horario_eventos, e.id_tipo_evento,
                   h.dia, h.hora_inicio, h.hora_fin, 
                   t.nombre AS tipo_evento
            FROM eventos.eventos e
            JOIN horarios.horario_eventos h ON e.id_horario_eventos = h.id
            JOIN eventos.tipo_evento t ON e.id_tipo_evento = t.id
            WHERE e.id = %s
        """, (id,))
        evento = cur.fetchone()

        # Obtener la lista de horarios para el dropdown
        cur.execute("SELECT id, CONCAT(dia, ' - ', hora_inicio, ' a ', hora_fin) AS horario FROM horarios.horario_eventos")
        horarios = cur.fetchall()

        # Obtener la lista de tipos de eventos
        cur.execute("SELECT id, nombre FROM eventos.tipo_evento")
        tipos_evento = cur.fetchall()

        cur.close()

        return render_template('app/eventos/editar_evento.html', evento=evento, horarios=horarios, tipos_evento=tipos_evento)
    
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')



#-------------------ACTUALIZA EL EVENTO-----------------------------

@eventos.route('/update_evento/<id>', methods=['POST'])
def update_evento(id):
    if 'loggedin' in session:
        if request.method == 'POST':
            nombre = request.form['nombre']
            id_horario_evento = request.form['id_horario_evento']
            direccion = request.form['direccion']
            id_tipo_evento = request.form['id_tipo_evento']
            fecha = request.form['fecha']

            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("""
                UPDATE eventos.eventos
                SET nombre = %s, id_horario_eventos = %s, direccion = %s, id_tipo_evento = %s, fecha = %s
                WHERE id = %s
            """, (nombre, id_horario_evento, direccion, id_tipo_evento, fecha, id))
            
            conn.commit()
            flash('¡Cambios guardados con éxito!')
            return redirect(url_for('eventos.ver_eventos'))
        
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')

#-----------------------ELIMINAR EVENTO-----------------------

@eventos.route('/deleteevento/<string:id>', methods=['POST', 'GET'])
def delete_evento(id):
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
                DELETE FROM eventos.eventos WHERE id = %s
                """, (id,))
        conn.commit()
        flash('Evento Eliminado Correctamente')
        return redirect(url_for('eventos.ver_eventos'))
    
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')
