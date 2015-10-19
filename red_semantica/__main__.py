#! /usr/bin/env python
import os.path
import argparse

from red_semantica.red import Net
from red_semantica.parser import Rule

def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='red_semantica',
        description=
        '''
            Creador de la red semantica.
            Por defecto el modulo lo que hace es generar un grafico utilizando
            la sintaxis dot de graphviz.
            Este grafico se podra dibujar con la herramienta 'dot'.
            Ejemplo: dot -Tps <archivo entrada> -o <archivo salida>
            Donde <archivo entrada> es un archivo que contiene la salida de
            este programa.
        '''
    )
    parser.add_argument(
        "conocimiento",
        help="Archivo de base de conocimiento",
        default=os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "conocimiento"
       ),
        nargs='?'
    )
    parser.add_argument(
        "-d", "--debug",
        action='store_true',
        help="Modo debug"
    )
    parser.parse_args()
    return parser.parse_args()

def main():
    args = parse_arguments()
    rules = Rule.fromFile(args.conocimiento)

    if args.debug: print(rules)

    net = Net.fromRules(rules)

    print(net.toString())

if __name__ == "__main__":
    exit(main())
