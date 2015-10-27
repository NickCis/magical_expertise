#! /usr/bin/env python3
import sys
import os.path
import argparse

from frames.frame import Frame
from frames.parser import FrameSet

def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='frames',
        description=
        '''
            Creador de frames.
            Importa la carpeta de frames especificados, los imprime.

        '''
    )
    parser.add_argument(
        "conocimiento",
        help="Carpeta de base de conocimiento",
        default=os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "example"
       ),
        nargs='?'
    )
    parser.add_argument(
        "-d", "--debug",
        action='store_true',
        help="Modo debug"
    )
    parser.add_argument(
        "-s", "--search",
        default=None,
        help="Importa este frame y busca con cual frame matchea",
        nargs='?'
    )
    parser.parse_args()
    return parser.parse_args()

def main():
    args = parse_arguments()
    set = FrameSet(args.conocimiento)
    set.importAll()

    if args.debug or not args.search:
        print(set)
        print()

    if args.search:
        print(">", args.search)
        input_frame = Frame.fromFile(args.search)
        print(input_frame)
        print("> Resultado:")

        for frame in set.frames.values():
            match = True
            for col in input_frame.getColumns():
                if input_frame.getValue(col) != frame.getValue(col):
                    match = False
                    break

            if match:
                print(frame)

if __name__ == "__main__":
    exit(main())
