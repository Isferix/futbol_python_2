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



db = {}

def fill_database(c=None):
    
    @SQL.connect(db['database'])
    def create_schema(c=c):

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

            # Clasificacion de datos
            city = []
            country = []
            tournament = []
            match = []
            for i in range(len(dataset)):
                [country.append((ciudad,)) for ciudad in [dataset[i]['home_team'], dataset[i]['away_team'], dataset[i]['country']]]

                city.append((dataset[i]['city'],))

                tournament.append((
                    dataset[i]['tournament'],
                    dataset[i]['neutral']
                ))

                match.append((
                    dataset[i]['date'],
                    country[0+(i*3)],
                    country[1+(i*3)],
                    dataset[i]['home_score'],
                    dataset[i]['away_score'],
                    tournament[i][0],
                    city[i],
                    country[2+(i*3)]
                ))

            # Purga de datos repetidos

            # Elegi purgar los datos despues de haberlos clasificados porque si lo hago al momento de clasificarlos
            # Las adiciones referenciales de listas que hago en match no funcionarian por que no existirian los 
            # indices buscados al borrarse los duplicados:
            #   country[0+(i*3)], country[1+(i*3)], etc...
            # Por el contrario, si no uso las adiciones referenciales estaria sobreañadiendo informacion,
            # es decir, repetiria expresiones como dataset[i][...] Esto haria que en la ejecucion se busque el mismo dato 2 veces o mas,
            # lo cual es ineficiente, para ello reciclo los datos que añadi antes, puesto que es mas facil recorrer una lista corta
            # que volver a recorrer el dataset entero

            clean_city = []
            [clean_city.append(ciudad) for ciudad in city if ciudad not in clean_city]

            clean_country = []
            [clean_country.append(pais) for pais in country if pais not in clean_country]

            clean_tournament = []
            [clean_tournament.append(torneo) for torneo in tournament if torneo not in clean_tournament]

            # Los partidos son irrepetibles, es imposible que exista un partido que haya ocurrido en la misma fecha entre 2 mismos paises
            # Por lo que no es necesario purgarlos (Dando por hecho que el .csv esta excento de errores)

            return {'city': clean_city, 'country': clean_country, 'tournament': clean_tournament, 'match': match}


    @SQL.connect(db['database'])
    def insert(dataset, c=c):
        c.executemany(
            """INSERT INTO ciudad(city)
            VALUES (?);""", dataset['city']
        )

        c.executemany(
            """INSERT INTO pais(country)
            VALUES (?)""", dataset['country'])

        print('Operacion 2 efectuada')
        c.executemany(
            """INSERT INTO torneo(tournament, neutral)
            VALUES (?, ?)""", dataset['tournament'])

        # print('Operacion 3 efectuada')
        # c.executemany("""
        # INSERT INTO partido(date, fk_home_team_pais, fk_away_team_pais, home_score, away_score, fk_tournmanet_torneo, fk_city_pais, fk_country_pais)
        # SELECT ?, ?, ?, ?, ?, ?, ?, ? 
        # FROM partido 
        # INNER JOIN pais AS p1 ON partido.fk_home_team_pais=p1.id 
        # INNER JOIN pais AS p2 ON partido.fk_away_team_pais=p2.id 
        # INNER JOIN pais AS p3 ON partido.fk_country_pais=p3.id
        # INNER JOIN torneo AS t ON partido.fk_tournmanet_torneo=t.id;""", dataset['match'])
    
    create_schema()

    dataset = fetch_data()

    insert(dataset)


def insert(time, name, heartrate):
    conn = sqlite3.connect(db['database'])
    c = conn.cursor()

    values = [time, name, heartrate]

    c.execute("""
        INSERT INTO heartrate (time, name, value)
        VALUES (?,?,?);""", values)

    conn.commit()
    # Cerrar la conexión con la base de datos
    conn.close()


def dict_factory(cursor, row):
    
    d = {col[0]:row[idx] for idx, col in enumerate(cursor.description)}
    
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def report(limit=0, offset=0, dict_format=False):
    # Conectarse a la base de datos
    conn = sqlite3.connect(db['database'])
    if dict_format is True:
        conn.row_factory = dict_factory
    c = conn.cursor()

    query = 'SELECT h_order.time, h_order.name, h_order.value as last_heartrate, \
             COUNT(name) as records \
             FROM (SELECT time, name, value FROM heartrate ORDER BY time) as h_order \
             GROUP BY name ORDER BY time'

    if limit > 0:
        query += ' LIMIT {}'.format(limit)
        if offset > 0:
            query += ' OFFSET {}'.format(offset)

    query += ';'

    c.execute(query)
    query_results = c.fetchall()

    # Cerrar la conexión con la base de datos
    conn.close()
    return query_results


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
