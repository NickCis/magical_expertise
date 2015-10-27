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

En `red_semantica/conocimiento` hay un ejemplo de la sintaxis. **Los nombres son case insensitive!.**

Basicamente se utiliza `nombre_relacion(nodos ...)`. La cantidad de nodos puede ser como maximo 3. Siendo la m&aacute;s comun 2.

Cuando hay solo dos nodos, se toma el primero como el nodo inicial, es decir el padre.

Cuando hay 3, se toma el nodo del medio como el padre.

## Frames

Esta carpeta contiene una implementacion de frames. Requiere tener instalado el paquete `yaml`.

    $ python -m frames -h
    usage: frames [-h] [-d] [-s [SEARCH]] [conocimiento]
    
    Creador de frames. Importa la carpeta de frames especificados, los imprime.
    
    positional arguments:
      conocimiento          Carpeta de base de conocimiento
    
    optional arguments:
      -h, --help            show this help message and exit
      -d, --debug           Modo debug
      -s [SEARCH], --search [SEARCH]
                            Importa este frame y busca con cual frame matchea
    
    $ python -m frames frames/example/
    ----
    Distribucion 1
    Lugar: Local 3, Sala 123
    Participantes: Sr. Adam, Sr. Braun, Sr. Schmidt
    Fecha: 21 Marzo 1986 10.00
    Tema: Distribucion
    ----
    Desarrollo
    Fecha: 21 Marzo 1986 10.00
    Tema: Desarrollo
    Lugar:
    Participantes:
    ----
    Distribucion
    Fecha: 21 Marzo 1986 10.00
    Tema: Distribucion
    Lugar:
    Participantes:
    ----
    Conferencia
    Fecha:
    Lugar:
    Tema:
    Participantes:
    
    $ python -m frames -s frames/search.yaml frames/example/
    > frames/search.yaml
    ----
    Search
    Fecha: 21 Marzo 1986 10.00
    Tema: Distribucion
    > Resultado:
    ----
    Distribucion 1
    Lugar: Local 3, Sala 123
    Participantes: Sr. Adam, Sr. Braun, Sr. Schmidt
    Fecha: 21 Marzo 1986 10.00
    Tema: Distribucion
    ----
    Distribucion
    Fecha: 21 Marzo 1986 10.00
    Tema: Distribucion
    Lugar:
    Participantes:

### Sintaxis de los frames

Se utilizo la sintaxis `yaml` para la construccion de un frame. Para especificar uno en un archivo debe contener los siguientes tags:

* `name`: nombre del frame
* `parent`: nombre del frame padre *(opcional)*
* `data`: todos los datos del frame

#### Ejemplo

    name: Distribucion
    parent: Conferencia
    data:
      - Fecha: 21 Marzo 1986 10.00
      - Tema: Distribucion
