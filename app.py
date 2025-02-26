from flask import Flask, jsonify, render_template, url_for, request, redirect, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from templates.web.web import web
from templates.app.personal.personal import personal
from templates.app.comentarios.comentarios import comentarios 
from templates.app.notificaciones.notificaciones import notificaciones 
from templates.app.conector import administrador
from templates.app.matriculas.matricula import matricula
from templates.app.horario_eventos.horario_eventos import horario_evento
from templates.app.tipo_evento.tipo_evento import tipo_evento
from templates.app.modalidad.modalidad import modalidad
from templates.app.eventos.eventos import eventos
from templates.app.matricula_evento.matricula_evento import matricula_evento

import psycopg2
import psycopg2.extras
import re
# Traer la conexion
from database.base import get_conection 
conn = get_conection()

app = Flask(__name__, static_url_path='/static')
app.secret_key = "capuli"

app.register_blueprint(web)

app.register_blueprint(personal)

app.register_blueprint(comentarios)

app.register_blueprint(notificaciones)

app.register_blueprint(administrador)

app.register_blueprint(matricula)

app.register_blueprint(horario_evento)

app.register_blueprint(tipo_evento)

app.register_blueprint(modalidad)

app.register_blueprint(eventos)

app.register_blueprint(matricula_evento)

# para cuando se cree una nueva base de datos
# hashed_password = generate_password_hash('1234')
# print("code",hashed_password)


# cerrar sesion
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('nombre_rol', None)
    session.pop('nombres', None)
    session.pop('apellidos', None)
    session.pop('fecha_nacimiento', None)
    session.pop('fecha_inscripcion', None)
    session.pop('nombre_cinturon', None)
    session.pop('genero', None)
    session.pop('correo', None)
    session.clear()
    # Redirect to login page
    return render_template('web/loginn.html')


if __name__ == '__main__':
    app.run(debug=True)