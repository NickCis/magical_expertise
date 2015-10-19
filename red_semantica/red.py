import re

class Net:
    def __init__(self):
        self.nodes = {}

    @staticmethod
    def fromRules(rules):
        net = Net()
        for rule in rules:
            net.addRule(rule)

        return net

    def searchNode(self, name):
        '''Busca un nodo por el nombre y lo devuelve. Si no existe, lo crea'''
        if not name in self.nodes:
            self.nodes[name] = Node(name)

        return self.nodes[name]

    def addRule(self, rule):
        padre = ''
        hijos = []

        if len(rule.objetos) == 3:
            padre = rule.objetos[1]
            hijos = [rule.objetos[0], rule.objetos[2]]
        else:
            padre = rule.objetos[0]
            hijos.append(rule.objetos[1])

        node = self.searchNode(padre)
        node.addRelation(Relation(rule.name, hijos))

    def toString(self):
        str = "digraph Red {\n"

        for key, value in self.nodes.items():
            str += value.toString()

        str += '}'

        return str

    def __repr__(self):
        return self.toString()

class Relation:
    '''Representa una relacion, como es direccional, solo guarda el nombre de la relacion y los nodos destino (hijos). La relacion va a estar guardada por el nodo inicio (padre), entonces no se guarda ese nodo en la relacion'''

    def __init__(self, name, nodes):
        self.name = name
        self.nodes = nodes

class Node:
    '''Representa un Nodo, cada nodo puede tener muchas relaciones. Las relaciones son dirigidas el nodo inicio (padre) es el que las guarda'''

    def __init__(self, name):
        self.name = name
        self.relations = []

    def addRelation(self, rel):
        self.relations.append(rel)

    def toString(self):
        def nameToDot(name):
            return ("node%s" % re.sub(r'\s', '_', name)).lower()

        def relNameToDot(rel):
            str = "rel%s" % nameToDot(rel.name)
            for n in rel.nodes:
                str += nameToDot(n)
            return str

        lines = [
            "%s [label=\"%s\"]" % (nameToDot(self.name), self.name)
        ]
        for rel in self.relations:
            lines.append("%s [label=\"%s\"]" % (
                nameToDot(rel.nodes[0]),
                rel.nodes[0]
            ))
            if len(rel.nodes) > 1:
                relName = relNameToDot(rel)
                lines.append("%s [label=\"%s\",shape=box]" % (
                    relName,
                    rel.name
                ))
                lines.append("%s -> %s" % (
                    nameToDot(self.name),
                    relName
                ))
                for n in rel.nodes:
                    lines.append("%s -> %s" % (
                        relName,
                        nameToDot(n)
                    ))
            else:
                lines.append("%s -> %s [label=\"%s\"]" % (
                    nameToDot(self.name),
                    nameToDot(rel.nodes[0]),
                    rel.name
                ))

        return "".join(["\t%s\n" % x for x in lines])


