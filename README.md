![Inove banner](/inove.jpg)
Inove Escuela de Código\
info@inove.com.ar\
Web: [Inove](http://inove.com.ar)

# Estadística del Fútbol [Python_2]

----------------------------------------------------------------------------------------------------------------
#27/9/2020:
__Armado de la estructura general de la API, se ha añadido:
- app.py
- config.py
- heart.py
- schema.sql

Estos archivos conforman la estructura general de la API y seran actualizados
con nuevas funcionalidades en los siguientes commits	

- \modulos\mySqlModule
- \static
- \templates

En estas carpetas se encuentran los recursos para renderizar las paginas y facilitar
interacciones con bases de datos
----------------------------------------------------------------------------------------------------------------




El programa consiste en realizar cálculos y estadística del fútbol internacional utilizando registros desde 1874. El programa consultará al usuario qué tipo de información desea obtener de un determinado equipo (ver detalle en salida del sistema).

Este proyecto está basado en el proyecto de Python Inicial:\
[https://github.com/InoveAlumnos/futbol_python_1](https://github.com/InoveAlumnos/futbol_python_1)

La diferencia radica en que ahora no se utilizará un CSV de entrada o de salida sinó que se solicitará transformar el CSV en una base de datos.

# Entrada del sistema
Debe tomar el “csv” con todos los resultados históricos de los partidos internacionales jugados desde 1874. Este archivo se lo proveerá al alumno, esa información el alumno la debe extraer y transformar en una base de datos.\
Luego el sistema debe aceptar por HTTP sumar nuevos resultados a la base de datos.

__Archivo CSV con los datos hístoricos de los partidos internacionales desde 1874 para transformar en DB__\
partidos.csv

# Salida del sistema
El usuario indicará al programa por HTTP de que país desea obtener información y analizará la base de datos. Posibles cálculos que podría realizar el sistema (el alumno puede agregar más resultados que desee al programa):
- Determinar cuántas veces ganó un país de local o de visitante.
- Determinar cuántas veces perdió un país de local o de visitante.
- Determinar cómo le fue al país en los últimos “N” partidos jugados (ejemplo, resultados de los últimos 10 partidos, ¿ganó la mayoría?
- Contra quien jugó el último partido de local o de visitante.
- Como le fue al país históricamente jugando contra otro país indicado.\

El reporte de estos resultados solicitados debe brindarse al usuario con una respuesta HTTP.

# Notas
Este proyecto puede utilizarse como base o referencia para hacer uno parecido o distinto del mismo tema. Se solicita que el contenído mínimo del proyecto alcance los especificado en las "entradas y salida del sistema" pudiendo el alumno modificar o agregar requerimientos. El objetivo en este proyecto es que construyan una base de datos, trabajen los datos y por último retornar una respuesta HTTP con un reporte.\
En cada caso puntual se discutirá con el alumno como puede ser modificado el proyecto según sus deseos o necesidades.

Estos temas se discuten en el campus del curso en el foro correspondiente al proyecto. Cada alumno deberá iniciar un tema de discucisión sobre el proyecto que desea realizar y como este lo desea implementar.

# Consultas
alumnos@inove.com.ar



