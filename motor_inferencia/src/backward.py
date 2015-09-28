import re

class Rule:
    def __init__(self, premisas, conclusion):
        self.premisas = premisas
        self.conclusion = conclusion
        self.disparada = False

    def __repr__(self):
        aux = ""
        for premisa in self.premisas:
            aux += premisa
        aux += "->"
        aux += self.conclusion
        return aux;

    def disparo(self,conocimientoAcertado):
        conocimientoAcertado.append(self.premisas)
        self.disparada = True
        print "se cumple: ",self.premisas

    def getUncheckedPremisa(self,baseConocimiento):
        for premisa in self.premisas:
            premisaVerificada = False
            for conocimiento in baseConocimiento:
                if (premisa == conocimiento):
                    premisaVerificada = True
                    break
            if not (premisaVerificada):
                return premisa


class Hipotesis:
    def __init__(self,hipotesis):
        self.hipotesis = hipotesis
        self.verificada = False

    def __repr__(self):
        return self.hipotesis

    def matchRule(self,rules):
        for rule in rules:
            if self.hipotesis == rule.conclusion:
                if (rule.disparada == False):
                    return rule
            continue
        return None

    def matchBase(self, baseConocimiento):
        for b in baseConocimiento:
            if self.hipotesis == b:
                return True
            continue
        return False


#esto deberia estar en un regex pero no me salio, no such fucking group
def parsePremisas(s):
    v = []
    for char in s:
        if not (char == 'y' or char == '\t' or char == ' ' or char == '\n'):
            v.append(char)
    return v


def backtrack(baseConocimiento,conocimientoAcertado):
    for h in hipotesis:
        print "verificando hipotesis : %s" % h
        if (h.matchBase(baseConocimiento)):
            print "ingrese un conocimiento sin verificar"
        else:
            rule = h.matchRule(rules)
            print "matching de: ",h
            print "descubro la regla: ",rule
            if not (rule is None):
                premisa = rule.getUncheckedPremisa(baseConocimiento)
                if not (premisa is None):
                    print "premisa que no esta en base: ",premisa
                    print "agrego premisa %s sin verificar a las hipotesis" % premisa;
                    hipotesis.append(Hipotesis(premisa))
                else:
                    rule.disparo(conocimientoAcertado);
                    hipotesis.remove(h)
                    baseConocimiento.append(rule.conclusion)
                    backtrack(baseConocimiento,conocimientoAcertado)


def loadRules():
    filename =  raw_input('Ingrese el nombre de la base de conocimiento: ')
    rules = []
    with open(filename) as f:
        for line in f:
            searchObj = re.search(r"^\s*si\s*(.*?),\s*entonces\s*(.*?)$",line)
            premisas = parsePremisas(searchObj.group(1))
            conclusion = searchObj.group(2)
            rules.append(Rule(premisas,conclusion))
    return rules


rules = loadRules()
print rules
baseConocimiento = ["p","q","r"]
conocimientoAcertado = []

h1 = Hipotesis("v")
hipotesis = [h1]
backtrack(baseConocimiento,conocimientoAcertado)

print "verificando %s, se encontro este conocimiento: %s" % (hipotesis,conocimientoAcertado)
