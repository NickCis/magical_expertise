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



baseConocimiento = ["p","q","r"]
conocimientoAcertado = []
r1 = Rule(["p","q"] , "s")
r2 = Rule(["r"] , "t")
r3 = Rule(["s","t"] , "u")
r4 = Rule(["s","r"] , "v")
rules = [r1,r2,r3,r4]


h1 = Hipotesis("v")
hipotesis = [h1]
backtrack(baseConocimiento,conocimientoAcertado)

print "verificando %s, se encontro este conocimiento: %s" % (hipotesis,conocimientoAcertado)
