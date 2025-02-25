from flask import Flask, jsonify, render_template, url_for, request, redirect, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import flask
import psycopg2
import psycopg2.extras
import re

from database.base import get_conection
conn = get_conection()

administrador = flask.Blueprint('administrador', __name__)

@administrador.route('/templates/app/admin.html')
def admin():
    if 'loggedin' in session:
       cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Obtener el número de notificaciones
       cursor.execute("SELECT COUNT(*) FROM personas.notificaciones")
       count = cursor.fetchone()[0]

         # Obtener el número de notificaciones
       cursor.execute("SELECT COUNT(*) FROM personas.comentarios")
       count_comentario = cursor.fetchone()[0]

      # Obtener el número de eventos
       cursor.execute("SELECT COUNT(*) FROM eventos.eventos")
       count_evento = cursor.fetchone()[0]

        # Obtener el número de estudiantes
       cursor.execute("SELECT COUNT(*) FROM personas.personas WHERE nombre_rol = 'Estudiante'")
       countt = cursor.fetchone()[0]

       return render_template('app/admin.html', countt=countt, count=count, count_comentario=count_comentario, count_evento=count_evento)
    
    # El usuario no ha iniciado sesión, redirigir a la página de inicio de sesión

    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')


@administrador.route('/templates/app/estudiante.html')
def estudiante():
    if 'loggedin' in session:

       cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

       cursor.execute("SELECT COUNT(*) FROM personas.notificaciones")
       count = cursor.fetchone()[0]
    
       return render_template('app/estudiante.html', count=count)
       
    # El usuario no ha iniciado sesión, redirigir a la página de inicio de sesión

    flash('Debes iniciar sesión para acceder a esta página.')
    return render_template('web/loginn.html')



@administrador.route('/templates/app/entrenador.html')
def entrenador():
   if 'loggedin' in session:
      return render_template('app/entrenador.html')
   flash('Debes iniciar sesión para acceder a esta página.')
   return render_template('web/loginn.html')
    