#!/usr/bin/env python
'''
Heart DB manager
---------------------------
Autor: Inove Coding School
Version: 1.1

Descripcion:
Programa creado para administrar la base de datos de registro
de pulsaciones de personas
'''

__author__ = "Inove Coding School"
__email__ = "alumnos@inove.com.ar"
__version__ = "1.1"

import os
from modulos import mySqlModule as SQL
from collections import OrderedDict

import sqlite3
import csv
import datetime



db = {}

def fill_database(c=None, conn=None):
    
    @SQL.connect(db['database'])
    def create_schema(c=c, conn=None):

        script_path = os.path.dirname(os.path.realpath(__file__))
        schema_path_name = os.path.join(script_path, db['schema'])

        c.executescript(open(schema_path_name, "r").read())


    def fetch_data():
        """
        Recorre un archivo csv y recolecta datos\n
        Return: Devuelve una lista con tuplas
        """
        with open(db['dataset'], encoding="utf-8") as csvfile:
            dataset = list(csv.DictReader(csvfile))

            # Desempaquetando la info
            data = [(
                x['date'],
                x['home_team'],
                x['away_team'],
                x['home_score'],
                x['away_score'],
                x['tournament'],
                x['city'],
                x['country'],
                x['neutral']) for x in dataset]

            # Agregando los ganadores y encapsulando la info en tuplas
            refined_data = []
            for i in data:
                refined_row = []
                [refined_row.append(x) for x in i]
                if int(i[3]) > int(i[4]):
                    refined_row.append(1)
                elif int(i[3]) < int(i[4]):
                    refined_row.append(0)
                else:
                    refined_row.append(2)
                refined_data.append(tuple(refined_row))
            return refined_data


    @SQL.connect(db['database'])
    def insert(dataset, c=None, conn=None):
        c.executemany(
            """INSERT INTO partido(date,home_team,away_team,home_score,away_score,tournament,city,country,neutral,result)
            VALUES(?,?,?,?,?,?,?,?,?,?);""", dataset)

    
    create_schema()

    dataset = fetch_data()

    insert(dataset)


def dict_factory(cursor, row):
    
    d = {col[0]:row[idx] for idx, col in enumerate(cursor.description)}
    
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def report_countrys(limit=0, offset=0, dict_format=False):
    @SQL.connect(db['database'])
    def function(limit, offset, c=None, conn=None):
        if dict_format is True:
            conn.row_factory = dict_factory

        query = 'SELECT home_team, away_team, result FROM partido ORDER BY home_team'

        if limit > 0:
            query += ' LIMIT {}'.format(limit)
        if offset > 0:
            query += ' OFFSET {}'.format(offset)

        query += ';'

        c.execute(query)
        query_results = c.fetchall()
        
        wins_draws_loses_dict = {}
        for row in query_results:
            equipo_1 = row[0]
            equipo_2 = row[1]
            ganador = row[2]
            if equipo_1 not in wins_draws_loses_dict:
                wins_draws_loses_dict[equipo_1] = [0, 0, 0]
            if equipo_2 not in wins_draws_loses_dict:
                wins_draws_loses_dict[equipo_2] = [0, 0, 0]

            #Punteros
            pe_1 = wins_draws_loses_dict[equipo_1] # Equipo 1
            pe_2 = wins_draws_loses_dict[equipo_2] # Equipo 2
            if ganador == 1:
                wins_draws_loses_dict[equipo_1] = [pe_1[0]+1, pe_1[1], pe_1[2]]
                wins_draws_loses_dict[equipo_2] = [pe_2[0], pe_2[1], pe_2[2]+1]
            elif ganador == 0:
                wins_draws_loses_dict[equipo_1] = [pe_1[0], pe_1[1], pe_1[2]+1]
                wins_draws_loses_dict[equipo_2] = [pe_2[0]+1, pe_2[1], pe_2[2]]
            else:
                wins_draws_loses_dict[equipo_1] = [pe_1[0], pe_1[1]+1, pe_1[2]]
                wins_draws_loses_dict[equipo_2] = [pe_2[0], pe_2[1]+1, pe_2[2]]
        wins_draws_loses_list = [{'country': x[0], 'wins': x[1][0], 'draws': x[1][1], 'loses': x[1][2]} for x in wins_draws_loses_dict.items()]
        return wins_draws_loses_list
    return function(limit, offset)


def chart(name):
    # Conectarse a la base de datos
    conn = sqlite3.connect(db['database'])
    c = conn.cursor()

    # Busco los ultimos 250 registro a nombre de name

    c.execute('''SELECT * FROM (SELECT time FROM heartrate
                 WHERE name =? ORDER by time desc LIMIT 250)
                 ORDER by time''', [name])

    query_output = c.fetchone()
    if query_output is None:
        # No data register
        # Bug a proposito dejado para poner a prueba el traceback
        # ya que el sistema espera una tupla
        return []

    time = query_output[0]
    # Extraigo el "time" del registro 250, y busco todos los registros
    # a su nombre cuyo tiempo sea mayor o igual al de ese registro
    c.execute('''SELECT time, value FROM heartrate
                WHERE name =? AND time >=?''', [name, time])

    query_results = c.fetchall()

    # Cerrar la conexión con la base de datos
    conn.close()

    # Extraigo la informacion en listas
    time = [x[0] for x in query_results]
    heartrate = [x[1] for x in query_results]

    return time, heartrate
