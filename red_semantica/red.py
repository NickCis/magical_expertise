
class Rule:
    def __init__(self,relacion,objetos):
        self.relacion = relacion
        self.objetos = objetos

    def __repr__(self):
        aux = ""
        aux += self.relacion
        aux += "->"
        aux += ''.join(self.objetos)
        return aux;

    def match(self,rule):
        for objeto in rule.objetos:
            if objeto in self.objetos:
                return True
        return False

class Node:

    #un nodo tiene una relacion para con el padre
    #e.g perro es un mamifero
    def __init__(self,objeto,padre,relacion):
        self.objeto = objeto
        self.padre = padre
        self.relacion = relacion
        self.children = []


class Net:

    def __init__(self,objeto):
        self.root = Node(objeto,None,None)
    #Evalua si se encuentra el nodo con el nombro objeto
    #returns el nodo con ese objeto

    def contains(self,objeto,nodo=None):
        if nodo is None:
            nodo = self.root

        if nodo is None:
            return None

        if nodo.objeto == objeto:
            return nodo
        else:
            for nodo in nodo.children:
                contains(objeto,nodo)

    def addNodo(nodoPadre, nodoHijo):
        nodoPadre.children.append(nodoHijo)


def buildNet(rules):
    net = Net(rules[0].objetos[1])
    for rule in rules:
        for objeto in rule.objetos:
            print(objeto)
            nodoHijo = net.contains(objeto)
            print(nodoHijo)
            if not nodoHijo is None:
                if net.contains(objeto):
                    #se esta repitiendo
                    pass
                else:
                    net.addNodo(Node(objeto[1],None,rule.relacion))
                    print("agrego")
            nodoPadre = net.contains(objeto[1])
            #seguir




def loadRules():
    from parser import loadRules

    rules = loadRules("conocimiento")
    return rules

def main():
    rules = loadRules()
    net = buildNet(rules)


if __name__ == "__main__":
	main()
	
