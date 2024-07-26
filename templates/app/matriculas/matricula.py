from flask import Flask, jsonify, render_template, url_for, request, redirect, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import flask
import psycopg2
import psycopg2.extras
import re

from database.base import get_conection
conn = get_conection()

matricula = flask.Blueprint('matricula', __name__)


@matricula.route('/templates/app/matriculas/nueva_matricula.html')
def nueva_matricula():
    if 'loggedin' in session:
        curc = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        curpro = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sc = "SELECT id, nombres || ' ' || apellidos as nombre_completo FROM personas.personas WHERE nombre_rol = 'Estudiante'"
        #spro = "SELECT * FROM personas.modalidades"
        curc.execute(sc)
        #curpro.execute(spro)
        list_cpersonas = curc.fetchall()
        #list_cmodalidades = curpro.fetchall()
        return render_template('app/matriculas/nueva_matricula.html', list_cpersonas=list_cpersonas)
    return render_template('web/loginn.html')






@matricula.route('/buscar_estudiante/<string:cedula>', methods=['GET'])
def buscar_estudiante(cedula):
    # Realizar la consulta a la base de datos para obtener los datos del estudiante
    # según la cédula proporcionada
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "SELECt id, nombres, apellidos, fecha_nacimiento, fecha_inscripcion, nombre_cinturon, genero, nombre_rol, correo, telefono, direccion FROM personas.personas WHERE id = %s"
    cur.execute(query, (cedula,))
    estudiante = cur.fetchone()

    if estudiante:
        # Devolver los datos del estudiante como respuesta JSON
        # Formatear las fechas en el formato "YYYY-MM-DD"
        estudiante['fecha_nacimiento'] = estudiante['fecha_nacimiento'].strftime("%Y-%m-%d") if estudiante['fecha_nacimiento'] else None
        estudiante['fecha_inscripcion'] = estudiante['fecha_inscripcion'].strftime("%Y-%m-%d") if estudiante['fecha_inscripcion'] else None
        return jsonify({'id': estudiante['id'],
                         'nombres': estudiante['nombres'],
                           'apellidos': estudiante['apellidos'],
                             'fecha_nacimiento': estudiante['fecha_nacimiento'],
                               'fecha_inscripcion': estudiante['fecha_inscripcion'],
                                 'nombre_cinturon':  estudiante['nombre_cinturon'],
                                   'genero':  estudiante['genero'],
                                     'nombre_rol':  estudiante['nombre_rol'],
                                       'correo':  estudiante['correo'],
                                         'telefono':  estudiante['telefono'],
                                           'direccion':  estudiante['direccion']})
    else:
        return jsonify({'error': 'Estudiante no encontrado'})


#---------------------------------HACER UNA MATRICULA---------------------------------

