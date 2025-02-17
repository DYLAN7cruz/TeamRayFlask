from flask import Flask, jsonify, render_template, url_for, request, redirect, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import flask
import psycopg2
import psycopg2.extras
import pandas as pd
from openpyxl.styles import Alignment
from fpdf import FPDF
from flask import send_file
from openpyxl import load_workbook


import re

from database.base import get_conection
conn = get_conection()

matricula_evento = flask.Blueprint('matricula_evento', __name__)

# Ruta para mostrar la página de nueva matrícula
@matricula_evento.route('/templates/app/matricula_evento/nueva_matricula_evento.html')
def nueva_matricula():
    if 'loggedin' in session:
        curc = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # Obtener los estudiantes para mostrar en el formulario
        sc = "SELECT id, nombres || ' ' || apellidos as nombre_completo FROM personas.personas WHERE nombre_rol = 'Estudiante'"
        curc.execute(sc)
        list_cpersonas = curc.fetchall()

        # Obtener la lista de horarios disponibles
        curc.execute("SELECT id, nombre FROM eventos.modalidad")
        modalidad = curc.fetchall()

        curc.execute("""SELECT e.id, e.nombre, CONCAT(h.dia, ' - ', h.hora_inicio, ' a ', h.hora_fin) AS "HORARIO EVENTO", e.direccion, t.nombre AS "TIPO EVENTO", e.fecha FROM eventos.eventos e JOIN horarios.horario_eventos h ON e.id_horario_eventos = h.id JOIN eventos.tipo_evento t ON e.id_tipo_evento = t.id;""")
        eventos = curc.fetchall()

        return render_template('app/matricula_evento/nueva_matricula_evento.html', list_cpersonas=list_cpersonas, modalidad=modalidad, eventos=eventos)
    flash("Debes iniciar sesión para acceder a esta página.")
    return render_template('web/loginn.html')

# Ruta para buscar un estudiante por cédula
@matricula_evento.route('/buscar_estudiante/<string:cedula>', methods=['GET'])
def buscar_estudiante(cedula):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = """
        SELECT id, nombres, apellidos, fecha_nacimiento, fecha_inscripcion, 
               nombre_cinturon, genero, nombre_rol, correo, telefono, direccion
        FROM personas.personas 
        WHERE id = %s AND nombre_rol = 'Estudiante'
    """
    cur.execute(query, (cedula,))
    estudiante = cur.fetchone()

    if estudiante:
        estudiante['fecha_nacimiento'] = estudiante['fecha_nacimiento'].strftime("%Y-%m-%d") if estudiante['fecha_nacimiento'] else None
        return jsonify({
            'id': estudiante['id'],
            'nombres': estudiante['nombres'],
            'apellidos': estudiante['apellidos'],
            'fecha_nacimiento': estudiante['fecha_nacimiento'],
            'genero': estudiante['genero']
        })
    else:
        return jsonify({'error': 'Estudiante no encontrado'})
    
# Ruta para registrar una nueva matrícula
@matricula_evento.route('/registrar_matricula_evento', methods=['POST'])
def registrar_matricula_evento():
    if 'loggedin' in session:
        try:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            # Obtener los datos del formulario
            id_personas = request.form.get('id_personas')
            id_eventos = request.form.get('id_eventos')
            id_modalidad = request.form.get('id_modalidad')
            peso = request.form.get('peso')

            print(f"Datos recibidos: id_personas={id_personas}, id_eventos={id_eventos}, id_modalidad={id_modalidad}, peso={peso}")

            if not id_personas or not id_eventos or not id_modalidad or not peso:
                flash("Todos los campos son obligatorios")
                return redirect(url_for('matricula_evento.nueva_matricula')) 

            cur.execute("SELECT * FROM personas.personas WHERE id = %s AND nombre_rol = 'Estudiante'", (id_personas,))
            estudiante = cur.fetchone()

            if not estudiante:
                flash("El estudiante no existe o no es válido.")
                return redirect(url_for('matricula_evento.nueva_matricula'))  

            cur.execute("SELECT * FROM eventos.matricula_evento WHERE id_personas = %s", (id_personas,))
            matricula_existente = cur.fetchone()

            if matricula_existente:
                flash("El estudiante ya está matriculado en un evento.")
                return redirect(url_for('matricula_evento.nueva_matricula'))  

            cur.execute("""
                INSERT INTO eventos.matricula_evento (id_personas, id_eventos, id_modalidad, peso)
                VALUES (%s, %s, %s, %s)
            """, (id_personas, id_eventos, id_modalidad, peso))

            conn.commit()
            flash("¡Matrícula registrada con éxito!")

        except Exception as e:
            conn.rollback()
            flash(f"Error al registrar la matrícula: {e}")

        return redirect(url_for('matricula_evento.ver_matriculas')) 

    flash("Debes iniciar sesión para acceder a esta página.")
    return render_template('web/loginn.html')

# Ruta para listar las matrículas
@matricula_evento.route('/templates/app/matricula_evento/matricula_evento.html', methods=['POST', 'GET'])
def ver_matriculas():
    """Endpoint para obtener la lista de matrículas con datos completos de eventos"""
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if request.method == "POST" and 'buscar' in request.form and request.form['buscar'].strip():
            # Consulta para buscar por id_personas
            search_term = '%' + request.form['buscar'].strip() + '%'
            s = """
                SELECT me.id, me.id_personas, p.nombres || ' ' || p.apellidos AS nombre_completo,
                       EXTRACT(YEAR FROM AGE(p.fecha_nacimiento)) AS edad,
                       e.nombre AS evento, 
                       TO_CHAR(h.hora_inicio, 'HH12:MI AM') || ' a ' || TO_CHAR(h.hora_fin, 'HH12:MI AM') AS horario_evento,
                       m.nombre AS modalidad, 
                       me.peso || ' kg' AS peso
                FROM eventos.matricula_evento me
                LEFT JOIN personas.personas p ON me.id_personas = p.id
                LEFT JOIN eventos.eventos e ON me.id_eventos = e.id
                LEFT JOIN horarios.horario_eventos h ON e.id_horario_eventos = h.id
                LEFT JOIN eventos.modalidad m ON me.id_modalidad = m.id
                WHERE me.id_personas LIKE %s
            """
            cur.execute(s, (search_term,))
        else:
            # Mostrar todas las matrículas
            s = """
                SELECT me.id, me.id_personas, p.nombres || ' ' || p.apellidos AS nombre_completo,
                       EXTRACT(YEAR FROM AGE(p.fecha_nacimiento)) AS edad,
                       e.nombre AS evento, 
                       TO_CHAR(h.hora_inicio, 'HH12:MI AM') || ' a ' || TO_CHAR(h.hora_fin, 'HH12:MI AM') AS horario_evento,
                       m.nombre AS modalidad, 
                       me.peso || ' kg' AS peso
                FROM eventos.matricula_evento me
                LEFT JOIN personas.personas p ON me.id_personas = p.id
                LEFT JOIN eventos.eventos e ON me.id_eventos = e.id
                LEFT JOIN horarios.horario_eventos h ON e.id_horario_eventos = h.id
                LEFT JOIN eventos.modalidad m ON me.id_modalidad = m.id
                ORDER BY e.id ASC
            """
            cur.execute(s)

        matriculados = cur.fetchall()
        cur.close()

        return render_template('app/matricula_evento/matricula_evento.html', matriculados=matriculados)

    flash("Debes iniciar sesión para acceder a esta página.")
    return render_template('web/loginn.html')

# eliminar la matricula
@matricula_evento.route('/delete_matricula_evento/<string:id>', methods=['POST', 'GET'])
def delete_matricula_evento(id):
    if 'loggedin' in session:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("DELETE FROM eventos.matricula_evento WHERE id = %s", (id,))
        conn.commit()
        print(id)
        flash('Matricula Eliminada Correctamente') 
        return redirect(url_for('matricula_evento.ver_matriculas'))
    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')

# Ruta para exportar las matrículas a Excel con ajuste de columnas
@matricula_evento.route('/exportar_matriculas_evento_excel', methods=['GET'])
def exportar_matriculas_evento_excel():
    if 'loggedin' in session:
        try:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            # Consulta para obtener todas las matrículas
            cur.execute("""
                SELECT me.id_personas, p.nombres || ' ' || p.apellidos AS nombre_completo,
                       EXTRACT(YEAR FROM AGE(p.fecha_nacimiento)) AS edad,
                       m.nombre AS modalidad, 
                       me.peso || ' kg' AS peso
                FROM eventos.matricula_evento me
                LEFT JOIN personas.personas p ON me.id_personas = p.id
                LEFT JOIN eventos.modalidad m ON me.id_modalidad = m.id
            """)
            matriculas = cur.fetchall()

            # Crear un DataFrame de pandas con formato
            df = pd.DataFrame(matriculas, columns=['Cédula', 'Nombre Completo', 'Edad', 'Modalidad', 'Peso'])

            # Exportar a un archivo Excel
            excel_file = 'matriculas.xlsx'
            df.to_excel(excel_file, index=False, engine='openpyxl')

            # Ajustar el ancho de las columnas y centrar el texto
            wb = load_workbook(excel_file)
            ws = wb.active

            # Ajustar el ancho de las columnas
            for col in ws.columns:
                max_length = 0
                col_letter = col[0].column_letter  # Obtener la letra de la columna
                for cell in col:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                    # Centrar el contenido de cada celda
                    cell.alignment = Alignment(horizontal='center', vertical='center')
                ws.column_dimensions[col_letter].width = max_length + 2  # Margen adicional
            
            # Guardar el archivo
            wb.save(excel_file)

            # Devolver el archivo como descarga
            return flask.send_file(excel_file, as_attachment=True)
        except Exception as e:
            print(f"Error al exportar matrículas a Excel: {e}")
            flash("Error al exportar las matrículas.")
            return redirect(url_for('matricula_evento.ver_matriculas'))
    else:
        flash("Debes iniciar sesión para acceder a esta página.")
        return render_template('web/loginn.html')