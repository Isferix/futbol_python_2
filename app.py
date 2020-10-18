#!/usr/bin/env python
'''
API Monitor cardíaco
---------------------------
Autor: Inove Coding School
Version: 1.0
 
Descripcion:
Se utiliza Flask para crear un WebServer que levanta los datos de
las personas que registran su ritmo cardíaco.

Ejecución: Lanzar el programa y abrir en un navegador la siguiente dirección URL
NOTA: Si es la primera vez que se lanza este programa crear la base de datos
entrando a la siguiente URL
http://127.0.0.1:5000/reset

Ingresar a la siguiente URL para ver los endpoints disponibles
http://127.0.0.1:5000/
'''

__author__ = "Inove Coding School"
__email__ = "INFO@INOVE.COM.AR"
__version__ = "1.0"

# Realizar HTTP POST --> https://www.codepunker.com/tools/http-requests

import traceback
import io
import sys
import os
import base64
import json
import sqlite3
from datetime import datetime, timedelta
from config import config

# Obtener la path de ejecución actual del script
script_path = os.path.dirname(os.path.realpath(__file__))

# Obtener los parámetros del archivo de configuración
config_path_name = os.path.join(script_path, 'config.ini')
db = config('db', config_path_name)
server = config('server', config_path_name)

import numpy as np
from flask import Flask, request, jsonify, render_template, Response, redirect
import matplotlib
matplotlib.use('Agg')   # For multi thread, non-interactive backend (avoid run in main loop)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg

import heart


heart.db = db
app = Flask(__name__)


@app.route("/")
def index():
    try:
        # Imprimir los distintos endopoints disponibles
        result = "<h1>Bienvenido!!</h1>"
        result += "<h2>Endpoints disponibles:</h2>"
        result += "<h3>[GET] /reset --> borrar y crear la base de datos</h3>"
        result += "<h3>[GET] /paises?limit=[]&offset=[] --> mostrar estadisticas del rendimiento de cada pais (limite and offset are optional)</h3>"
        result += "<h3>[GET] /paises/tabla?limit=[]&offset=[] --> mostrar estadisticas del rendimiento de cada pais en una tabla</h3>"
        result += "<h3>[GET] /{pais}/tabla?limit=[]&offset=[] --> mostrar últimas partidos jugados (limite and offset are optional)</h3>"
        result += "<h3>[GET] /{pais}/historico --> mostrar el rendimiento histórico de de un pais</h3>"
        result += "<h3>[GET][POST] /registro --> HTML con el formulario de registro de un nuevo partido para añadir a la database</h3>"

        return(result)
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/reset")
def reset():
    try:
        # Borrar y crear la base de datos
        heart.fill_database()
        result = "<h3>Base de datos re-generada!</h3>"
        return (result)
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/paises")
def paises():
    try:
        return render_template('tabla.html')
    except:
        return jsonify({'trace': traceback.format_exc()})

@app.route("/paises/tabla")
def paises_tabla():
    try:
        result = show(heart.report_countrys)
        return (result)
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/<pais>/tabla")
def pais_tabla(pais):
    try:
        result = show(heart.report_country(pais))
        return (result)
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/<pais>/historico")
def pais_historico(pais):
    try:
        # Obtener el historial de la persona
        time, heartrate = heart.chart(pais)

        # Crear el grafico que se desea mostrar
        fig, ax = plt.subplots(figsize=(16, 9))
        ax.plot(time, heartrate)
        ax.get_xaxis().set_visible(False)

        output = plot_to_canvas(fig)
        plt.close(fig)  # Cerramos la imagen para que no consuma memoria del sistema
        return Response(output.getvalue(), mimetype='image/png')
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/registro", methods=['GET', 'POST'])
def registro():
    if request.method == 'GET':
        try:
            return render_template('registro.html')
        except:
            return jsonify({'trace': traceback.format_exc()})

    if request.method == 'POST':
        try:
            # Alumno: Implemente
            # Obtener del HTTP POST JSON el nombre y los pulsos
            name = request.form.get('name')
            age = request.form.get('age')
            nationality = request.form.get('nationality')

            persona.insert(name, int(age), nationality)
            return Response(status=200)
        except:
            return jsonify({'trace': traceback.format_exc()})


def show(function, show_type='table'):
    limit_str = str(request.args.get('limit'))
    offset_str = str(request.args.get('offset'))

    if(limit_str is not None) and (limit_str.isdigit()):
        limit = int(limit_str)
    else:
        limit = 0
    if(offset_str is not None) and (offset_str.isdigit()):
        offset = int(offset_str)
    else:
        offset = 0

    data = function(limit, offset, dict_format=True)

    if show_type == 'json':
        return jsonify(data)
    elif show_type == 'table':
        return html_table(data)
    else:
        return jsonify(data)


def html_table(data):

    # Tabla HTML, header y formato
    result = '<table border="1">'
    result += '<thead cellpadding="1.0" cellspacing="1.0">'
    result += '<tr>'
    result += '<th>Nombre</th>'
    result += '<th>Fecha</th>'
    result += '<th>Último registro</th>'
    result += '<th>Nº de registros</th>'
    result += '</tr>'

    for row in data:
        # Fila de una tabla HTML
        result += '<tr>'
        for i in range(len(row)):
            result += '<td>' + str(i) + '</td>'
        result += '</tr>'

    # Fin de la tabla HTML
    result += '</thead cellpadding="0" cellspacing="0" >'
    result += '</table>'

    return result


def plot_to_canvas(fig):
    # Convertir ese grafico en una imagen para enviar por HTTP
    # y mostrar en el HTML
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return output


def html_table(data):

    # Tabla HTML, header y formato
    result = '<table border="1">'
    result += '<thead cellpadding="1.0" cellspacing="1.0">'
    result += '<tr>'
    result += '<th>Pais</th>'
    result += '<th>Ganados</th>'
    result += '<th>Empates</th>'
    result += '<th>Perdidos</th>'
    result += '</tr>'

    for row in data:
        # Fila de una tabla HTML
        result += '<tr>'
        for i in row.keys():
            result += '<td>' + str(row[i]) + '</td>'
        result += '</tr>'

    # Fin de la tabla HTML
    result += '</thead cellpadding="0" cellspacing="0" >'
    result += '</table>'

    return result


if __name__ == '__main__':

    heart.fill_database()

    app.run(host=server['host'],
            port=server['port'],
            debug=True)
