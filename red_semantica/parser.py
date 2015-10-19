import re

class Rule:
    def __init__(self, name, objetos):
        self.name = name
        self.objetos = [x for x in objetos]

    @staticmethod
    def fromString(line):
        '''Crea la regla apartir de la representacion de texto'''
        rule = None
        match = re.search(r'^([^(]+)\(([^)]+)\)', line)
        if not match:
            raise SyntaxError("Sintaxis de regla invalida")

        relacion = match.group(1).strip()
        objetos = [x.strip() for x in match.group(2).split(',')]
        if len(objetos) <= 3:
            rule = Rule(relacion, objetos)
        else: # no se aceptan mas de 3 objetos en una regla
            raise ValueError("La regla no puede tener mas de 3 argumentos")

        return rule

    @staticmethod
    def fromFile(filename):
        '''Abre el archivo, lo parsea y devuelve una lista de reglas'''
        rules = []
        with open(filename) as f:
            for line in f:
                rules.append(Rule.fromString(line))
        return rules

    def __repr__(self):
        return "%s(%s)" % (self.name, ', '.join(self.objetos))

    def match(self, rule):
        for objeto in rule.objetos:
            if objeto in self.objetos:
                return True
        return False
