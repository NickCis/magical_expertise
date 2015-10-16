import re
from red import Rule


def loadRules(filename):
    filename
    rules = []
    with open(filename) as f:
        for line in f:
            searchObj = re.search(r'(^\w+)\((\w.*)\)',line)
            relacion = searchObj.group(1)
            objetos = searchObj.group(2)
            objetos = objetos.split(',',objetos.count(','))
            if len(objetos) == 2:
                rules.append(Rule(relacion,objetos))
            # no se aceptan mas de 3 objetos en una regla
            elif len(objetos) == 3:
                rules.append(Rule(relacion,[objetos[1],objetos[0]]))
                rules.append(Rule(relacion,[objetos[1],objetos[2]]))
    return rules


