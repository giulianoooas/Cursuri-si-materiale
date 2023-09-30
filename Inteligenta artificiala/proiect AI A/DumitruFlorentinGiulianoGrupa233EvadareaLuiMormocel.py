"""
    Dumitru Florentin Giuliano
    grupa 233
    Proiect 1
    Evadarea lui Mormocel
"""


from math import sqrt
from time import time
from random import randint

class Frunza:
    """
        O clasa ce ma ajuta sa retin toate informatiile necesare unei frunze, mai exact
        id-ul , coordonatele , greutatea maxima si numarul de insecte
    """
    def __init__(self, id, x, y, nrInsecte = 0, greutateMaxima = 0):
        self.id = id
        self.x = x
        self.y = y
        self.nrInsecte = nrInsecte
        self.greutateMaxima = greutateMaxima
    
    def __str__(self):
        afis = f"Id: {self.id}\nCoordonate: ({self.x},{self.y})\nIar greutatea maxima este: {self.greutateMaxima}\nNumarul de insecte este {self.nrInsecte}\n"
        return afis
    
    def copie(self):
        """
            Aceasta functie imi returneaza o copie a obiectului meu
        """
        return Frunza(self.id,self.x,self.y,self.nrInsecte,self.greutateMaxima)
    
    def distanta(self): # returneaza distanta pana la orgine a frunzei
        return sqrt(self.x**2 +self.y**2)

class Info:
    """
        O clasa ajutatoare pentru a defini informatia in nod
        retine informatiile necesare frunzei si greutatea actuala a broscutei
    """
    def __init__(self, frunza, greutate):
        self.greutate = greutate
        self.frunza = frunza
    
    def __str__(self):
        afis = ""
        afis += "Greutatea broastei este " + str(self.greutate)
        afis += "\n"
        afis += str(self.frunza)
        return afis

class NodParcurgere:
    def __init__(self, info, parinte, cost=1, h=0, frunze = [], insecte = 0):
        """
            Info practic represinta instanta clasei info in cazul nodului meu, adica retine toate datele frunzei si greutatea actuala a broscutei
            frunze reprezinta o lista de frunze, mai exact cum arata frunzele pana in punctul respectiv in fiecare nod
            insecte reprezinte numarul de insecte mancate de broscuta in nodul tata
        """
        self.info = info# info = (pozitia actuala a broscutei si greutate)
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost
        self.h = h
        self.f = self.g + self.h
        self.frunze = [i.copie() for i in frunze]
        self.insecte = insecte
    
    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def contineInDrum(self,info):
        return info.id in [i.info.frunza.id for i in self.obtineDrum()]
    
    def afisDrum(self):
        """
            Aici am facut functia de afisare dupa cum imi cere enuntul.
            folosind stringul special f'sas', pentru o susurinta la formatare
        """
        l = self.obtineDrum()
        n = len(l)
        afis = ""
        for j in range(n):
            afis += f"{j+1})"
            i = l[j]
            greutate = i.info.greutate 
            try:
                greutate += l[j+1].insecte
            except:
                pass
            if i.parinte == None:
                afis += f"Broscuta se afla pe frunza initiala {i.info.frunza.id}({i.info.frunza.x},{i.info.frunza.y}).\nGreutate broscuta: {greutate}"
            elif i.info.frunza.id == "Afara":
                afis += f"Broscuta a ajuns la mal in {j} sarituri.\n"
            else:
                afis += f"Broscuta sarit de la {i.parinte.info.frunza.id}({i.parinte.info.frunza.x},{i.parinte.info.frunza.y}) la {i.info.frunza.id}({i.info.frunza.x},{i.info.frunza.y}).\n"
                try:
                    if l[j+1].insecte != 0:
                        afis+= f"Broscuta a mancat {l[j+1].insecte} insecte. "
                except:
                    pass
                afis += f"Greutate broscuta: {greutate}"
            afis += "\n"
        afis += "\n"
        return afis
            

    def calculeazaDistanta(self):
        return sqrt(self.info.frunza.x ** 2 + self.info.frunza.y ** 2)

    def __str__(self):
        string = str(self.info)
        string += f"\nCostul este {self.f}\n"
        return string
    
class Graph:
    def __init__(self, nume_fisier):
        cin = open(nume_fisier, "r")
        """
            Am verificat daca datele citite sunt corecte pentr- un try si except 
            daca apare vreo frunza mai ce nu se afla pe lac sau broasca are grreutatea mai mica sau egalad ecat 0 
            sau  raza este negativa
        """
        try:
            date = cin.read()
            cin.close()
            date = date.split("\n")
            self.raza = int(date[0])
            if self.raza <= 0:
                raise "raza negativa"
            self.greutate = int(date[1])
            if self.greutate <= 0:
                raise "greutate negativa"
            self.idStart = date[2]
            self.Frunze = []
            for i in date[3:]:
                j = i.split()
                id = j[0]
                x = int(j[1])
                y = int(j[2])
                nrInsecte = int(j[3])
                greutateMaxima = int(j[4])
                fr = Frunza(id,x,y,nrInsecte,greutateMaxima)
                if fr.distanta() > self.raza:
                    raise "Nu se afla pe lac"
                self.Frunze.append(fr)
            self.start = Info([i for i in self.Frunze if i.id == self.idStart][0],self.greutate)

            """
                inca o verificare ce trebuie facuta este daca greutatea broscutei este mai mare decat greutatea maxima ce poate sa fie
                pe frunza de start, daca da, este o problema cu datele introduse
            """
            if self.greutate > self.start.frunza.greutateMaxima:
                raise "Mormocel ar fi ajuns in apa!"

        except:
            self.raza = 0
            self.greutate = 0
            self.idStart = None
            self.Frunze = []
            self.start = None

    def distantaFrunza(self, x,y):
        return sqrt(x**2 + y ** 2)
    
    def testeaza_scop(self, nod):
        return nod.info.frunza.id == "Afara" # daca are acest id inseamna ca a iesit din lac
    
    def calculeaza_h(self, info, tip_euristica= 0):
        if tip_euristica == 0: # euristica banala
            if info.frunza.id == "Afara": # daca este solutie returnez o, altfel 1
                return 0
            return 1
        elif tip_euristica == 1: # eurstica mea definita, ce returneaza distanta de la nodul meu la malul lacului, facand raza - distanta la centru, si am impartit la raza pentru a obtine un numar intre 0 si 1
            return (self.raza-info.frunza.distanta())/self.raza
        elif tip_euristica == 2:
            return 1 / (1 + info.frunza.distanta())  # in cazul  euristicii acesteia, cu cat ma indepartez de centru(care are h = 1) euristica devine mai mica
        else:
            return info.greutate # aceasta este euristica neadmisibila
            """
                Nu este admisibila, deoarece nu este relevant daca are mai putine unitati de energie pentru a verifica distanta fata de mal.
                In urma acestei euristici programul ar putea considera ca este mai eficient sa sara catre centru decat catre mal, doar din cauza euristicii.
            """
    
    def calcDistanta(self,fr1,fr2):
        """
            Calculeaza distanta dintre doua frunze, practic puncte
        """
        return sqrt((fr1.x - fr2.x)**2 +(fr1.y - fr2.y)**2 )


    def genereazaSuccesori(self,nodCurent,tip_euristica = 0):
        if nodCurent.info.frunza.id == "Afara":
            return []
        """ 
            Daca nodul meu curent este o solutie atunci nu ii mai fac succesorii, acest lucru verific aici
            prin id-ul frunzei sa fie egal cu Afara
            id-ul Afara este cel specific pentru solutii
        """
        nr_insecte = 0
        poz = 0
        limita = 0
        for i in range(len(nodCurent.frunze)):
            """
                Acest for imi va afla cate insecte pot manca de pe frunza curenta fara sa depasesc limita, si o sa tin minte si limita pentru a verifica mai usor
            """
            if nodCurent.frunze[i].id == nodCurent.info.frunza.id:
                nr_insecte = nodCurent.frunze[i].nrInsecte
                poz = i
                limita = nodCurent.frunze[i].greutateMaxima
        
        l = []
        for i1 in range(nr_insecte + 1): # aici incerc sa mananc cat de multe insercte de pe frunza actuala, de la 0 pana unde imi perminte pentru a nu depasi greutateea maxima
            greutate = nodCurent.info.greutate  + i1
            if greutate > limita: # daca am depasit limita ma opresc
                break
            if greutate <= 0: # daca greutatea este negativa continui
                continue
            frunze = [i.copie() for i in nodCurent.frunze] 
            """ 
                aici fac o copie fiecarei frunze, pentru a o putea trimite fiecarui copil,
                mai exact frunza ce pleaca din nodul curent
                daca nu faceam copia asa, aveam problema cu datele
            """
            frunze[poz].nrInsecte -= i1 # aici scad  din frunza nodului curent numarul de insecte de aici
            for j in range(len(frunze)):
                if (not nodCurent.contineInDrum(frunze[j])) and (greutate - 1 <= frunze[j].greutateMaxima) and (greutate/3 >= self.calcDistanta(frunze[poz],frunze[j])) and (greutate > 1):
                    """
                        Acest if verifica in primul rand daa in urma pierderii unei unitati de energie in urma saroturii poate sa stea pe frunza destinatie fara sa se scufunde,
                        daca frunza respectiva nu a mai fost vizitata de drumul nodului curent
                        si daca poate sa sara pana acolo
                    """
                    inf = Info(frunze[j], greutate-1)
                    cost =  1 + nodCurent.g
                    h = self.calculeaza_h(inf,tip_euristica)
                    nodActual = NodParcurgere(inf,nodCurent,cost,h,frunze, i1)
                    l.append(nodActual)
            if (greutate/3 >= self.raza - nodCurent.calculeazaDistanta()) and (greutate > 1): # aici verific daca pot sari pe mal direct, automat are eurstica 0
                """
                    In cazul  in care am reusit de pe o frunza sa sar direct pe mal
                    voi face id-ul malului "Afara", iar coordonatele vor fi (raza,0)
                """
                cost = nodCurent.g + 1
                info = Info(Frunza("Afara", self.raza,0),greutate-1)
                h = self.calculeaza_h(info,tip_euristica)
                nodActual = NodParcurgere(info,nodCurent,cost,h,[],i1)
                l.append(nodActual)
        
        return l

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return sir
    
    def showFrunze(self):
        for i in self.Frunze:
            print(str(i))
    
    def dateleSuntBune(self):
        """
            Functia aceasta verifica daca datele de intrare sunt, verificand daca starea initiala este diferita de None
        """
        return self.start != None

numarNoduritotal, maxLungimeCoada,res,gasitSolutie = 0,0, "", False

def a_star(gr, nrSolutiiCautate, tip_euristica = 1):
    global numarNoduritotal, maxLungimeCoada,res,gasitSolutie
    if gr.start == None:
        return
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    numarNoduritotal = 1
    maxLungimeCoada = 1
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start, tip_euristica), gr.Frunze)]
    while len(c) > 0:
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            gasitSolutie = True
            res += "\n"
            res += nodCurent.afisDrum()
            res += "\n"
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        numarNoduritotal += len(lSuccesori)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # diferenta fata de UCS e ca ordonez dupa f
                if c[i].f >= s.f:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)
        maxLungimeCoada = max(maxLungimeCoada,len(c))


def a_star_eficient(gr, tip_euristica = 1):
    global numarNoduritotal, maxLungimeCoada, res,gasitSolutie
    if gr.start == None:
        return
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start, tip_euristica), gr.Frunze)]
    closed = []
    numarNoduritotal = 1
    maxLungimeCoada = 1
    while len(c) > 0:
        nodCurent = c.pop(0)
        closed.append(nodCurent)

        if gr.testeaza_scop(nodCurent):
            gasitSolutie = True
            res += "\n"
            res += nodCurent.afisDrum()
            res += "\n"
            return

        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica)
        numarNoduritotal += len(lSuccesori)
        lSuccesoriCopy = lSuccesori.copy()
        for s in lSuccesoriCopy:
            gasitOpen = False
            for elem in c:
                if s.info == elem.info:
                    gasitOpen = True
                    if s.f < elem.f:
                        c.remove(elem)
                    else:
                        lSuccesori.remove(s)
                    break
            if not gasitOpen:
                for elem in closed:
                    if s.info == elem.info:
                        if s.f < elem.f:
                            closed.remove(elem)
                        else:
                            lSuccesori.remove(s)
                        break

        for s in lSuccesori:
            i = 0
            while i < len(c):
                if c[i].f >= s.f:
                    break
                i += 1
            c.insert(i, s)
        maxLungimeCoada = max(maxLungimeCoada,len(c)) 


def ida_star(gr, nrSolutiiCautate, tip_euristica = 1):
    global numarNoduritotal, maxLungimeCoada, res,gasitSolutie
    if gr.start == None:
        return
    limita = gr.calculeaza_h(gr.start,tip_euristica)
    nodStart = NodParcurgere(
        gr.start, None, 0, limita, gr.Frunze
    )
    numarNoduritotal = 1
    maxLungimeCoada = 0
    while True:
        nrSolutiiCautate, rez = construieste_drum(
            gr, nodStart, limita, nrSolutiiCautate,tip_euristica
        )
        if rez == "gata":
            break
        if rez == float("inf"):
            break
        limita = rez


def construieste_drum(gr, nodCurent, limita, nrSolutiiCautate,tip_euristica):
    global numarNoduritotal, maxLungimeCoada, res,gasitSolutie
    if nodCurent.f > limita:
        return nrSolutiiCautate, nodCurent.f

    if gr.testeaza_scop(nodCurent) and nodCurent.f == limita:
        gasitSolutie = True
        res += "\n"
        res += nodCurent.afisDrum()
        res += "\n"
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return nrSolutiiCautate, "gata"

    lSuccesori = gr.genereazaSuccesori(nodCurent,tip_euristica)
    numarNoduritotal += len(lSuccesori)
    maxLungimeCoada = max(maxLungimeCoada, len(lSuccesori))
    minim = float("inf")
    for s in lSuccesori:
        nrSolutiiCautate, rez = construieste_drum(gr, s, limita, nrSolutiiCautate,tip_euristica)
        if rez == "gata":
            return nrSolutiiCautate, "gata"
        if rez < minim:
            minim = rez
    return nrSolutiiCautate, minim

def uniform_cost(gr, nrSolutiiCautate=1, tip_euristica = 1):
    global numarNoduritotal, maxLungimeCoada, res,gasitSolutie
    if gr.start == None:
        return
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None, 0,0,gr.Frunze)]
    numarNoduritotal = 1
    maxLungimeCoada = 1
    while len(c) > 0:
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            gasitSolutie = True
            res += "\n"
            res += nodCurent.afisDrum()
            res += "\n"
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent,tip_euristica)
        numarNoduritotal += len(lSuccesori)
        for s in lSuccesori:
            i = 0
            while i < len(c):
                if c[i].g > s.g:
                    break
                i += 1
            c.insert(i, s)
        maxLungimeCoada = max(maxLungimeCoada,len(c))

def alageOEuristica():
    return randint(0,3) # imi va returna random o euristica dintre cele definite de mine

def unNumarDeSolutii():
    return randint(1,5) # imi va returna un numar random intre 1 si 3

if __name__ == "__main__":   

    """
        Am facut 2 list de fisiere, primul pentru fisierele de tip input, iar a doua pentru cele de tip output
        in fisierul de tip output voi afisa res ce este rezultatul pentru fiecare dintre cazuri
        Voi genera random cate o euristica pentru fiecare dintre cazuri
    """ 
    inputs = ["file1.txt", "file2.txt", "file3.txt","file4.txt"]
    outputs = ["out1.txt", "out2.txt", "out3.txt", "out4.txt"]
    for j in range(4):
        i = inputs[j]
        o = outputs[j]
        g = Graph(i)
        if g.dateleSuntBune():
            res = ""

            numarNoduritotal, maxLungimeCoada,gasitSolutie = 0,0,False
            res += "Algoritmul A*:\n"
            euristica = alageOEuristica()
            nrSolutii = unNumarDeSolutii()
            res += f"Euristica folosita este {euristica}\nNumarul de solutii cautate este {nrSolutii}\n"
            start = time()
            a_star(g,nrSolutii,euristica)
            end = time()
            if not gasitSolutie:
                res += "\nProblema n-are solutie!\n\n"
            res += f"Timul necesar rularii algoritmului A* : {end - start}\nNumarul total de noduri folosit : {numarNoduritotal}\nNumarul maxim de noduri in coada : {maxLungimeCoada}\n\n"

            numarNoduritotal, maxLungimeCoada,gasitSolutie = 0,0,False
            res += "Algoritmul A* eficient:\n"
            euristica = alageOEuristica()
            res += f"Euristica folosita este {euristica}\n"
            start = time()
            a_star_eficient(g,euristica)
            end = time()
            if not gasitSolutie:
                res += "\nProblema n-are solutie!\n\n"
            res += f"Timul necesar rularii algoritmului A* eficient : {end - start}\nNumarul total de noduri folosit : {numarNoduritotal}\nNumarul maxim de noduri in coada : {maxLungimeCoada}\n\n"

            numarNoduritotal, maxLungimeCoada,gasitSolutie = 0,0,False
            res += "Algoritmul UCP:\n"
            euristica = alageOEuristica()
            nrSolutii = unNumarDeSolutii()
            res += f"Euristica folosita este {euristica}\nNumarul de solutii cautate este {nrSolutii}\n"            
            start = time()
            uniform_cost(g,nrSolutii,euristica)
            end = time()
            if not gasitSolutie:
                res += "\nProblema n-are solutie!\n\n"
            res += f"Timul necesar rularii algoritmului UCP : {end - start}\nNumarul total de noduri folosit : {numarNoduritotal}\nNumarul maxim de noduri in coada : {maxLungimeCoada}\n\n"

            numarNoduritotal, maxLungimeCoada,gasitSolutie = 0,0,False
            res +="Algoritmul IDA*:\n"
            euristica = alageOEuristica()
            nrSolutii = unNumarDeSolutii()
            res += f"Euristica folosita este {euristica}\nNumarul de solutii cautate este {nrSolutii}\n"
            start = time()
            ida_star(g,nrSolutii,euristica)
            end = time()
            if not gasitSolutie:
                res += "\nProblema n-are solutie!\n\n"
            res += f"Timul necesar rularii algoritmului IDA* : {end - start}\nNumarul total de noduri folosit : {numarNoduritotal}\nNumarul maxim de noduri in coada : {maxLungimeCoada}\n\n"
        else:
            res = "Datele sunt gresite!"
        with open(o,"w+") as out:
            out.write(res)
        