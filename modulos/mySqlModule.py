'''
MongoDB [Python]
Libreria personalizada 
---------------------------
Autor: Inove Coding School
Version: 1.0

Descripcion:
Programa creado para facilitar la utilizacion de conexiones con TinyMongoDB
'''

__author__ = "Ishef Glatzel"
__email__ = "ishefglatzel@glatzel.com.ar"
__version__ = "1.0"


import sqlite3


def connect(file):
    """
    `Decorador` que encapsula una funcion en una conexion con una `database` `SQL`\n
    @param file: `str` Nombre del archivo al que se conectara la funcion

    NOTA: La funcion encapsulada `DEBE` tener un parametro keyword llamada `db`\n
    Esto es asi porque la funcion `execute` declara un objeto db, y al ejecutar
    la funcion, lo pasa como valor, al `argumento` `keyword` asociado a la clave `db`
    """

    def _connect(accion):
        """
        `Receptor` de la funcion del decorador\n
        @param accion: `func` Funcion encapsulada
        """

        def execute(*args, **kwargs):
            """
            Funcion clave del decorador\n
            Envuelve la funcion decorada en una conexion a la database pasada como parametro
            con formato:
            \t[conexion]
            \t[ejecucion]
            \t[desconexion]

            """
            
            
            conn = sqlite3.connect(file)    
            c = conn.cursor()
        
            returns = accion(c=c, *args, **kwargs)

            conn.commit()
            conn.close()

            return returns

        return execute

    return _connect