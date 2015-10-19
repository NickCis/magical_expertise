import re

class Rule:
    def __init__(self, name, objetos):
        self.name = name
        self.objetos = objetos

    @staticmethod
    def fromString(line):
        '''Crea la regla apartir de la representacion de texto'''
        rule = None
        searchObj = re.search(r'(^\w+)\((\w.*)\)', line)
        relacion = searchObj.group(1)
        objetos = [x.strip() for x in searchObj.group(2).split(',')]
        if len(objetos) <= 3:
            rule = Rule(relacion, objetos)
        else:
            # no se aceptan mas de 3 objetos en una regla
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
        aux = ""
        aux += self.name
        aux += "("
        aux += ', '.join(self.objetos)
        aux += ')'
        return aux;

    def match(self, rule):
        for objeto in rule.objetos:
            if objeto in self.objetos:
                return True
        return False
