# magical_expertise

Repositorio usado para la materia Sistemas Automaticos de Deteccion de Fallas 2. Facultad de ingenieria de la Uba. 2do Cuatrimestre 2015

## `motor_inferencia`

Esta carpeta contiene el motor de inferencia desarrollado en rust

## `red_semantica`

Esta carpeta contiene la red semantica desarrollada en python.

    $ python -m red_semantica -h
    usage: red_semantica [-h] [-d] [conocimiento]
    
    Creador de la red semantica. Por defecto el modulo lo que hace es generar un
    grafico utilizando la sintaxis dot de graphviz. Este grafico se podra dibujar
    con la herramienta 'dot'. Ejemplo: dot -Tps <archivo entrada> -o <archivo
    salida> Donde <archivo entrada> es un archivo que contiene la salida de este
    programa.
    
    positional arguments:
      conocimiento  Archivo de base de conocimiento
    
    optional arguments:
      -h, --help    show this help message and exit
      -d, --debug   Modo debug
    
    $ python -m red_semantica red_semantica/conocimiento > /tmp/grafico.dot
    $ dot -Tps /tmp/grafico.dot -o /tmp/grafico.ps
    $ evince /tmp/grafico.ps

### Sintaxis de la base de conocimiento

En `red_semantica/conocimiento` hay un ejemplo de la sintaxis.

Basicamente se utiliza `nombre_relacion(nodos ...)`. La cantidad de nodos puede ser como maximo 3. Siendo la m&aacute;s comun 2.

Cuando hay solo dos nodos, se toma el primero como el nodo inicial, es decir el padre.

Cuando hay 3, se toma el nodo del medio como el padre.
