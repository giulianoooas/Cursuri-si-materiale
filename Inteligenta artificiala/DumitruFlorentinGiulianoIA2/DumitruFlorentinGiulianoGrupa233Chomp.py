import tkinter as tk
import threading as th
from time import sleep, time
root = tk.Tk()
root.title("Chomp! Proiect Dumitru Florentin Giuliano")
limita = 12

"""
    locul unde imi voi declara 2 Frame-uri:
        1) pentru meniu, partea de inceput al jocului
        2) al doilea pentru partea cu jocul propiu zis
    
"""
dificultati = [1,2,3]
dificultati_nume = ["easy","mediu","hard"]

"""
    Adancimea cu care ma voi duce in algorimtii mei de cautare
"""

timp = 0
timoMinim, timpamixm, timpmediu, nrmutari = float("+inf"), float("-inf"), 0,0
noduriMin, noduriMax, noduriMediu = float("+inf"), float("-inf"), 0
play = False
ParteaDeInceput = None
ParteaDeJoc = None
ParteaDeAfisareCastigator = None
nrPlayeri = None
algoritmul = None
mutare = None
dificultate = None

"""
    variabila asta va vedea cati playeri am:
        0 = computer vs computer
        1 = player vs computer
        2 = player vs player
    variabila algoritmul va retine cu ce algoritm decid eu sa joc:
        minmax sau alfabeta
    variabila mutare va fi folosita pentru mutarea playerilor

    dificultate = imi va da dificultatea - easy, medium sau hard
"""

class Joc:
    players = ['R','B']
    players_name = ["Player1", "Player2"]

    def __init__(self,n,m, otravite):
            #Voi genera tabla de dimensiunile date, daca sunt valide, altfel pastrez cum erau definite in atributele generale ale clasei
        
        try:
            self.otravite = []
            self.m = 0
            self.n = 0
            self.table = []
            if n < 0 or m < 0:
                raise "Invalid dimensions"
            for i,j in otravite:
                if i < 0 or i >= n or j < 0 or j >= m:
                    raise "Ciocolata nu este bine data"
                    self.otravite.append((i,j))
            self.m = m
            self.n = n
            self.table = [[1 for i in range(m)] for j in range(n)]
            for (i,j) in otravite:
                self.table[i][j] = "X"
        except:
            pass
        finally:
            self.turn = 0 # eu voi fi playerul max
        self.castigator = None

    @classmethod
    def setPlayer1Name(cls,name): # functia ce-mi va seta numele primului player
        if name == "":
            return
        else:
            cls.players_name[0] = name

    @classmethod
    def setPlayer2Name(cls,name):# functia ce-mi va seta numele celui de-al doilea player
        if name == "":
            return
        else:
            cls.players_name[1] = name

    @classmethod
    def changeColors1(cls):
        if cls.players[0] == "R":
            cls.players[0] = "B"
            cls.players[1] = "R"

    @classmethod
    def changeColors2(cls):
        if cls.players[0] == "B":
            cls.players[0] = "R"
            cls.players[1] = "B"

    def __expandeaza(self,m,i,j):
        """
            O functie private ce ma va ajuta sa verific daca solutia gasita este valida
            prin expandare, adica fac nula pozitia din matrice a elementului m[i][j]
        """
        m[i][j] = 0

        if i < self.n - 1:
            if m[i+1][j] == 1:
                self.__expandeaza(m,i+1,j)
        
        if i >= 1:
            if m[i-1][j] == 1:
                self.__expandeaza(m,i-1,j)

        if j >= 1:
            if m[i][j-1] == 1:
                self.__expandeaza(m,i,j-1)

        if j < self.m - 1:
            if m[i][j+1] == 1:
                self.__expandeaza(m,i,j+1)

    def PlayerValidation1(self,i1,j1,i2,j2, turn = None):
        """
            Voi vedea daca este mutarea valida a playerului prin urmatoarele metode:
                1) voi vedea daca intre pozitiile primite se afla doar 1 
                2) construiesc mutarea partiala si vad sa nu rupa in 2 ciocolata
        """
        if turn  == None:
            turn = self.turn
        elif not turn in [0,1]:
            return False
        if 0 > i1 or 0 > i2 or 0 > j1 or 0 > j2:
            return False
        if self.n <= i1 or self.n <= i2 or self.m <= j1 or self.m <= j2:
            return False
        a = [i.copy() for i in self.table]
        for i in range(i1,i2 + 1):
            for j in range(j1,j2 + 1):
                if a[i][j] != 1:
                    return False
                a[i][j] = self.players[turn]
        
        return self.isValid(a)         

    def isValid(self,m):
        """
            verific daca solutia mea gasita este valida
            acest lucru il fac astfel:
                1) creez o matrice noua ce are doua valori: 1 daca este o casuta libera si 0 alfel
                2) folosesc nr ca un contor ce imi numara cate 'insuilte' imi gaseste
                Insulita reprezinta o portiune maximala numai de 1
                3) daca nr devine 2 returnez false, deoarece nu este o solutie valida
        """
        a = [[1 for i in range(self.m)] for j in range(self.n)]
        for i in range(self.n):
            for j in range(self.m):
                if m[i][j] != 1:
                    a[i][j] = 0

        nr = 0

        for i in range(self.n):
            for j in range(self.m):
                if a[i][j] == 1:
                    nr += 1
                    if nr == 2:
                        return False
                    self.__expandeaza(a,i,j)

        return True
    
    def Move(self, a = None, turn = None, estimare = 0, sorteaza = False,reverse = True):
        '''
            In functie de cine e la joc min sau max sortez fie crescator fie descrescator, dupa valoare.

            functia ce imi va returna toate posibilitatile de miscare de pe harta
            Optimizare:
                Voi verifica daca la pasul de mutare i +1 si j + 1 s-a gasit vreo solutie, daca nu, voi trece direct la pasul de mutare i + 2, 1,
                deoarece sigur nu poate gasi solutie la pasul de mutare i + 1 , j + 2
            
            parametrul sorteaza verifica daca este mutare pentru algoritmul alfaBeta, caz in care mi se sorteaza
        '''
        if turn != None and turn in [0,1]:
            pass
        else:
            turn = self.turn
        color = self.players[turn] # culoarea o voi seta cu randul persoanei
        
        res = []
        try:
            for i in range(0,self.n):
                gasit = True
                for j in range(0,self.m):
                    # Aceste 2 foruri imi vor verifica pentru fiecare mutare de orice lungime posibila
                    if gasit == False:
                        break
                    gasit = False
                    for i1 in range(self.n):
                        for j1 in range(self.m):
                            """
                                Aici vreau sa incerc sa plec de pe orice pozitie
                                daca mutarea este buna, atunci o adaug 
                            """
                            if a == None:
                                m = [copie.copy() for copie in self.table]
                            else:
                                m = [copie.copy() for copie in a]

                            ok = True
                            for index1 in range(i+1):
                                if i1 + index1 >= self.n:
                                    ok = False
                                    break
                                for index2 in range(j+1):
                                    if j1 + index2 >= self.m:
                                        ok = False
                                        break
                                    if m[i1 + index1][j1 + index2] != 1:
                                        ok = False
                                        break
                                    m[i1 + index1][j1 + index2] = color
                                else:
                                    if ok == False:
                                        break
                            if ok and self.isValid(m):
                                gasit = True
                                res.append([copie.copy() for copie in m])
        except:
            pass
        if sorteaza:
            if estimare == 0:
                res.sort(key = lambda a : self.Estimare1(a,rev),reverse = reverse)
                return res[:limita]
            else:
                res.sort(key = lambda a : self.Estimare2(a), reverse = reverse)
                return res[:limita]
        return res

    def castigaTabla(self,tabla):
        """
            Functia aceasta este de fapt functia ce va verifica daca o tabla primita este cea castigatoare
            acest lucru se face prin verificarea daca exista vreo valoare 1
            daca da, inseamna ca nu este castigatoare, altfel este
        """
        for i in tabla:
            for j in i:
                if j == 1:
                    return False
        return True

    def Estimare2(self,tabla,jmin):
        """
            Am 3 valori posibile returnate:
                1 - daca este castigatoare
                -1 - daca ma poate duce intr-o pozitie pierzatoare
                0 - altfel
        """
        if jmin:
            if self.castigaTabla(tabla):
                return 1
            for i in self.Move(tabla):
                if self.castigaTabla(i):
                    return - 1
            return 0
        else:
            if self.castigaTabla(tabla):
                return -1
            for i in self.Move(tabla):
                if self.castigaTabla(i):
                    return  1
            return 0

    def Estimare1(self,tabla, jmin): 
        """
            Aici voi avea 2 valori posibile returnate:
                100 - pentru o pozitie castigatoare
                scad 5 pentru fiecare pozitie ce ma poate face sa pierd
        """
        if jmin:
            if self.castigaTabla(tabla):
                return 100
            nr = 0
            for i in self.Move(tabla):
                if self.castigaTabla(i):
                    nr -= 5
            return nr
        else:
            if self.castigaTabla(tabla):
                return -100
            nr = 0
            for i in self.Move(tabla):
                if self.castigaTabla(i):
                    nr += 5
            return nr

    def showTable(self):
        for i in self.table:
            print(*i)
    
    def showMoves(self):
        moves = self.Move()
        for i,m in enumerate(moves):
            print(f"Mutarea posibila {i + 1}:")
            for j in m:
                print(*j)
            print()
    
    def makeMove(self, estimare = 0, player = False):
        """
            Ma voi folosi de clasa Node pentru a genera urmatoarele miscari
            asta in pentru computer vs computer sau player vs player
        """
        if player:
            if len(mutare) < 4:
                return self.table
            i1,j1,i2,j2 = tuple(mutare)

            if self.PlayerValidation1(i1,j1,i2,j2):
                for i in range(i1,i2 + 1):
                    for j in range(j1,j2 + 1):
                        self.table[i][j] = self.players[self.turn]
                self.castigat()
                self.turn = 1 - self.turn
                return True
            return False
            
        try:
            estimare = int(estimare) % 2
        except:
            estimare = 0
        
        a = Node(None,self.table,self,estimare)

        try:
            self.table= [i.copy() for i in a.makeNextMove(True).tabla]
            self.castigat()
            self.turn = 1 - self.turn
        except:
            return 
    
    def castigat(self):
        """
            Dupa orice mutare vrea sa verific daca meciul s-a terminat
            acest lucru il voi face retinand castigatorul
        """
        for i in range(self.n):
            for j in range(self.m):
                if self.table[i][j] == 1:
                    return 
        self.castigator = self.players_name[self.turn]

class Node:

    def __init__(self,parent,tabla,joc, estimare,turn = None,jmin = True):
        """
            clasa Node imi salveaza informatiile necesare aflarii urmatoarei mutari optime ale calculatorului
            in functie de estimarea pe care am dat- o
            variabila nrNoduriGenerate imi va retine numarul de noduri generate la fiecare pas din unul dintre cei doi algoitmi
        """
        self.nrNoduriGenerate = 0
        self.parent = parent
        self.joc = joc
        if turn  == None:
            self.turn = joc.turn
        else:
            self.turn = turn
        self.tabla = [i.copy() for i in tabla]
        if estimare == 0:
            self.score = joc.Estimare1(tabla,jmin)
        else:
            self.score = joc.Estimare1(tabla,jmin)
        self.estimare = estimare

    def MinMax(self,node,adancime,minmax):
        """
            Am aplicat algorimul MinMax
            Si in functie de minmax vad daca caut valoarea maxima dintre succesori sau minima
            la fel voi face si pentru alfabeta
        """
        if adancime <= 0:
            return node
        
        succesors = [Node(node,i,self.joc,node.estimare, 1 - node.turn,not node.jmin) for i in self.joc.Move(node.tabla,node.turn,self.turn,True,minmax)]
        self.nrNoduriGenerate += len(succesors)
        if len(succesors) == 0:
            return node

        if minmax:

            succesors = [self.MinMax(i,adancime-1,not minmax) for i in succesors]
            nodul = None
            for i in succesors:
                if nodul == None:
                    nodul = i
                elif nodul.score < i.score:
                    nodul = i
            return nodul
        else:
            
            succesors = [self.MinMax(i,adancime-1,not minmax) for i in succesors]
            nodul = None
            for i in succesors:
                if nodul == None:
                    nodul = i
                elif nodul.score > i.score:
                    nodul = i
            return nodul
    
    def AlfaBeta(self,node,adancime,minmax, alfa,beta):
        #diferenta dintre acest algoritm si minmax este optimizarea adusa de alfa si beta ce nu mai verifica nodurile inutile
        if adancime <= 0:
            return node
        
        succesors = [Node(node,i,self.joc,node.estimare, 1 - node.turn,not node.jmin) for i in self.joc.Move(node.tabla,node.turn,self.turn,True,minmax)]
        self.nrNoduriGenerate += len(succesors)
        if len(succesors) == 0:
            return node

        if minmax:

            succesors = [self.AlfaBeta(i,adancime-1,not minmax,alfa,beta) for i in succesors]
            nodul = None
            for i in succesors:
                if nodul == None:
                    nodul = i
                elif nodul.score < i.score:
                    nodul = i
                alfa = max(alfa,nodul.score)
                if alfa >= beta:
                    break
            if nodul == None:
                nodul = node
            return nodul
        else:
            succesors = [self.AlfaBeta(i,adancime-1,not minmax,alfa,beta) for i in succesors]
            nodul = None
            for i in succesors:
                if nodul == None:
                    nodul = i
                elif nodul.score > i.score:
                    nodul = i
                beta = min(alfa,nodul.score)
                if alfa >= beta:
                    break
            if nodul == None:
                nodul = node
            return nodul

    def makeNextMove(self,minmax):
        """
            Functia aceasta imi va face mutarea in functie de algorimtul ales la inceputul jocului,
            adica MinMax sau AlfaBeta
            tot aici imi voi actualiza variabilele globale pentru afisarea informatiilor jocului
            adica timpii si nodurile
        """
        global timpamixm,timpmediu,timoMinim,nrmutari,noduriMediu,noduriMax, noduriMin
        adancime = dificultati[dificultate]
        start = time()
        if algoritmul == "minmax":
            nodul = self.MinMax(self,adancime,minmax)
        else:
            nodul = self.AlfaBeta(self,adancime,minmax,float("-inf"),float("+inf"))
        stop = time()
        timp = stop - start
        timpamixm = max(timp,timpamixm)
        timoMinim = min(timp,timoMinim)
        timpmediu += timp
        nrmutari += 1
        noduriMax = max(self.nrNoduriGenerate,noduriMax)
        noduriMin = min(self.nrNoduriGenerate,noduriMin)
        noduriMediu += self.nrNoduriGenerate
        try:
            while nodul.parent.parent != None:
                nodul = nodul.parent
            return nodul
        except:
            return nodul

class Casuta:
    """
        O clasa ce ma va ajuta sa prelucrez mutarea mai usor, astfel:
            1) tabla de joc e facuta din butoane initial funtionale de culoare alba ce poate fi apasat
            2) orice buton de alta culoare va fi imposibil de apasat
            3) dupa o apasare a butonului returneaza 2 valori:
                -i - linia din tabla pe care o ocupa
                -j - coloana din tabla pe care o ocupa
            4) dupa ce a fost apasat butonul poate capata 2 culori:
                a) verde daca este primul buton apasat
                b) verde inchis daca este al doilea
    """
    def __init__(self, i, j, master):
        self.i = i
        self.j = j
        self.b = tk.Button(master, command = self.Command, text = "", height = 3, width = 6, state = "normal")
        self.b.grid(row = i, column = j)

    def Command(self):
        l = len(mutare)
        if l == 0:
            self.b.config(bg =  "green")
            mutare.extend([self.i,self.j])
        elif l == 2:
            self.b.config(bg =  "darkgreen")
            mutare.extend([self.i,self.j])
    
    def enable(self):
        self.b.config(state = "normal")
    
    def disable(self):
        self.b.config(state = tk.DISABLED)

    def coloreaza(self, color):
        """
            Tabletele negre nu pot fi apasate si inseamna zona otravita
        """
        if color == "X":
            self.b.config(state = tk.DISABLED, bg = "black")
        if color == "B":
            self.b.config(state = tk.DISABLED, bg = "blue")
        if color == "R":
            self.b.config(state = tk.DISABLED, bg = "red")
        if color == 1:
            self.b.config(bg = "white")
        
class Tabla:

    def __init__(self, joc, master = ParteaDeJoc):
        """
            Este clasa jocului propiu-zisa unde creez interfata grafica a tablei, mai exact butoanele de care am vorbit
            Aici am si 3 butoane cu functionalitati pe care mi le-a cerut proiectul:
                a) un buton ce-ti permite sa iei de la capat mutarea
                b) un buton ce-ti permite sa mergi la urmatoarea pentru a vedea fluid si repetarile pc-ului
                c) un buton ce-ti permite sa opresti fortat jocul
            
            Cand jocul se termina afisez 3 lucruri:
                a) cat timp a durat.
                b) tabla jocului
                c) castigatorul
                d) butonul de Reia daca vrei sa joci iar
        """
        global timp
        timp = 0 # timpul mereu trebuie sa porneasca de la 0
        self.zonaNume = tk.LabelFrame(master, text = "Player actual", padx = 10, pady = 10) #zona unde afisez : numele playerului ce joaca si timmer-ul
        self.zonaNume.pack(padx = 10, pady = 10)
        self.timer = tk.Label(self.zonaNume, text = "00:00")
        self.timer.pack(padx = 10., pady = 10)
        self.gata = False # o variabila ce verifica daca s-a terminat jocul
        th.Thread(target=self.startStopwatcher).start() # thread folosit pentru a face timmer-ul, ca sa se execute in paralel cu algoritmii
        self.Nume = tk.Label(self.zonaNume, text = "")
        self.Nume.pack()
        self.pozi = 0 # jucatorul actual
        self.joc = joc # primeste jocul curent
        self.zonaTabla = tk.LabelFrame(master, text = "Tabla de joc")
        self.zonaTabla.pack(padx = 10, pady = 10) 

        self.t1 = None # timmer player 1 ce va retine momentul de start al unei mutari
        self.t2 = None # timmer player 2 ce va retine momentul de stop al unei mutari
        # acestea 2 sunt folosit pentru a calcula cat timp dureaza o mutare a unui player
        self.tablete = [[Casuta(i,j,self.zonaTabla) for j in range(joc.m)] for i in range(joc.n)]
        self.actualizeazaTabla()

        self.next = tk.Button(master, text = "Urmatoarea miscare",command = self.start)
        self.next.pack(padx = 10,pady = 10)
        self.actualizeazaTabla()
        self.back = tk.Button(master, text = "Reincepe", command = self.Back)
        self.back.pack(padx = 10, pady = 10)
        self.stop = tk.Button(master, text = "Gata", command = self.Stop)
        self.stop.pack(padx = 10, pady = 10)
        self.Reia = tk.Button(ParteaDeAfisareCastigator, text = "Reia", command = self.destroy,font = (40,)) 
        #butonul de reia imi da posibilitatea de a relua jocul
    
    def afiseazaInformatii(self):
        """
            Afiseaza in consola toate informatiile necesare cerute:
                a) despre noduri
                b) despre timp
        """
        global nrmutari
        if nrmutari == 0:
            return
        if nrPlayeri == 0:
            print("S-a jucat computer vs computer.")
        elif nrPlayeri == 1:
            print("S-a jucat player vs computer.")
        else:
            print("S-a jucat player vs player.")

        print(f"Dificultatea pe care s-a jucat a fost : {dificultati_nume[dificultate]}")

        print("Timp maxim :",timpamixm,"Timp minim :",timoMinim, "Timp mediu :", timpmediu/nrmutari)
        print("Numarul de mutari:",nrmutari)
        if nrPlayeri <= 1:
            if nrmutari % 2 == 1  and nrPlayeri == 1 and nrmutari != 1:
                nrmutari -= 1
            print("Numarul total de noduri generate:", noduriMediu)
            print("Noduri maxim generate :",noduriMax,"noduri minim generate :",noduriMin, "Noduri mediu generate:", noduriMediu//nrmutari*(nrPlayeri + 1))

    def Stop(self):
        #functia ce va opri fortat jocul si afiseaza toate informatiile pana in punctul respectiv
        self.next.destroy()
        self.back.destroy()
        self.stop.destroy()
        self.Nume.destroy()
        self.afiseazaInformatii()
        self.gata = True
        self.Reia.pack(pady = 10)

    def destroy(self):
        #funtia aceasta distruge tabla de joc pentru a putea incepe unul nou
        self.zonaTabla.destroy()
        self.zonaNume.destroy()
        self.Reia.destroy()
        meniu()
    
    def startStopwatcher(self):
        """
            Functia cronometru ce ne ajuta sa numaram de cat timp se joaca si sa afisam asta playerilor
            Lucrul se face printr-un thread ce din 1ms intr-alta actualizeaza timpul
            Se opreste numai cand jocul este gata
        """ 
        global timp
        while self.gata == False:
            min = str(timp//60)
            if len(min) == 1:
                min = "0" + min
            sec = str(timp%60)
            if len(sec) == 1:
                sec = "0" + sec
            self.timer.config(text = f"{min}:{sec}")
            if self.gata:
                break # daca meciul s-a terminat ies fortat
            sleep(1)
            timp += 1
        
        #cand termin meciul afisez Jocul a durat si durata lui
        min = str(timp//60)
        if len(min) == 1:
            min = "0" + min
        sec = str(timp%60)
        if len(sec) == 1:
            sec = "0" + sec
        self.timer.config(text = f"Jocul  a durat {min}:{sec}")
        

    def Back(self):
        #ne reseteaza o mutare
        global mutare
        mutare = []
        for i in range(self.joc.n):
            for j in range(self.joc.m):
                if self.joc.table[i][j] == 1:
                    self.tablete[i][j].enable()
        self.actualizeazaTabla()

    def actualizeazaTabla(self):
        #functia aceasta regenereaza la fiecare pas tabla sau afiseaza cine a castigat si informatiile necesare
        if self.t1 == None:
            self.t1 = time()
        global ParteaDeAfisareCastigator
        if self.joc.castigator == None:
            self.Nume.config(text = self.joc.players_name[self.joc.turn])

        for i in range(self.joc.n):
            for j in range(self.joc.m):
                self.tablete[i][j].coloreaza(self.joc.table[i][j])
        self.joc.showTable()
        print()
        if nrPlayeri == 0 or (nrPlayeri == 1 and self.pozi == 1):
            self.makeDisable()
        else:
            self.makeEnable()
        
        if self.joc.castigator != None and self.gata == False:
            self.Nume.destroy()
            self.gata = True
            self.stop.destroy()
            print(f"A castigat {self.joc.castigator}")
            self.afiseazaInformatii()
            ParteaDeAfisareCastigator = tk.Frame(root,padx = 10, pady = 10)
            ParteaDeAfisareCastigator.pack()
            tk.Label(ParteaDeAfisareCastigator,text = f"Castigatorul este {self.joc.castigator}", font = (40,)).pack()
            self.next.destroy()
            self.back.destroy()
            self.Reia.pack(pady = 10)

    def makeDisable(self):
        for i in self.tablete:
            for j in i:
                j.disable()

    def makeEnable(self):
        for i in range(self.joc.n):
            for j in range(self.joc.m):
                if self.joc.table[i][j] == 1:
                    self.tablete[i][j].enable()

    def MutareCalculator(self):
        """
            Functia asta imi va face mutarea calculatorului
            in timpul mutarii calculatorului nu pot sa opresc meciul
            doar inainte sau dupa
        """
        self.stop.config(state = tk.DISABLED)
        self.back.config(state = tk.DISABLED)
        self.next.config(state = tk.DISABLED)
        self.Nume.config(text = f"{self.joc.players_name[self.joc.turn]} se gandeste...")
        self.joc.makeMove(self.pozi)
        self.pozi = 1 - self.pozi
        self.back.config(state = "normal")
        self.next.config(state = "normal")
        self.stop.config(state = "normal")
        self.actualizeazaTabla()

    def start(self):
        """
            in functie de pozitie si numarul de playeri, vede cine trebuie sa mute
            pentru mutarile playerilor se trece la urmatoarea mutare 
            numai in cazul in care mutarea este valida
        """
        global timpmediu,timoMinim,timpamixm,nrmutari
        """
            Am folosit threaduri pentru miscarile calculatorului, deoarece nu stiu cat de mult poate sa dureze asteptarea 
            si nu vreau sa mi se blocheze jocul
        """
        if nrPlayeri == 0:
            th.Thread(target=self.MutareCalculator).start()
        elif nrPlayeri == 1 and self.pozi == 1:
            th.Thread(target=self.MutareCalculator).start()
        else:
            global mutare
            if len(mutare) == 4:
                if mutare[0] > mutare[2]:
                    mutare[0],mutare[2] = mutare[2],mutare[0]
                if mutare[1] > mutare[3]:
                    mutare[1],mutare[3] = mutare[3],mutare[1]
                val = self.joc.makeMove(1, True)
                if val == False:
                    self.Back()
                    return
                self.t2 = time()
                timp = self.t2 - self.t1
                self.pozi = 1 - self.pozi
                timpamixm = max(timp,timpamixm)
                timoMinim = min(timp,timoMinim)
                timpmediu += timp
                self.t1 = None
                nrmutari += 1
                mutare = []
                self.actualizeazaTabla()
                return

        mutare = []

def makeJoc():# functia ce-mi va genera jocul
    joc = Joc(4,4,[(0,2),(1,1)])
    tabla = Tabla(joc)

def meniu(): 
    global ParteaDeInceput,ParteaDeJoc, ParteaDeAfisareCastigator,nrPlayeri,algoritmul,mutare,dificultate
    if ParteaDeJoc != None:
        ParteaDeJoc.destroy()
        ParteaDeJoc = None
    if ParteaDeAfisareCastigator !=None:
        ParteaDeAfisareCastigator.destroy()
        ParteaDeAfisareCastigator = None

    ParteaDeInceput = tk.Frame(root,padx = 10, pady = 10)
    ParteaDeInceput.pack()
    """
        Aceasta este functia ce-mi va seta numele playerilor
        Imi va alege cu ce algoritm joc
        si modul de joc
    """
    nrPlayeri = 1
    algoritmul = "minmax"
    mutare = []
    dificultate = 0

    def b1():
        global nrPlayeri
        nrPlayeri = 2
        buttonPlayerVsPlayer.config(state = tk.DISABLED)
        buttonPlayerVsComputer.config(state = "normal")
        buttonComputerVsComputer.config(state = "normal")

    def b2():
        global nrPlayeri
        nrPlayeri = 1
        buttonPlayerVsPlayer.config(state = "normal")
        buttonPlayerVsComputer.config(state = tk.DISABLED)
        buttonComputerVsComputer.config(state = "normal")
    
    def b3():
        global nrPlayeri
        nrPlayeri = 0
        buttonPlayerVsPlayer.config(state = "normal")
        buttonComputerVsComputer.config(state = tk.DISABLED)
        buttonPlayerVsComputer.config(state = "normal")


    AlegePlayer = tk.LabelFrame(ParteaDeInceput, text = "Alege Numarul de Playeri",padx = 20,pady = 20)
    AlegePlayer.pack( pady = 5)
    buttonPlayerVsPlayer = tk.Button(AlegePlayer, text = "Player vs Player", command = b1)
    buttonPlayerVsPlayer.grid(row = 0, column = 0,padx = 6,pady = 3)
    buttonPlayerVsComputer = tk.Button(AlegePlayer, text = "Player vs Computer", command = b2, state = tk.DISABLED)
    buttonPlayerVsComputer.grid(row = 0, column = 1, padx = 6, pady = 3)
    buttonComputerVsComputer = tk.Button(AlegePlayer, text = "Computer vs Computer", command = b3)
    buttonComputerVsComputer.grid(row = 0, column = 2, padx = 6, pady = 3)

    """
        Aici am creat butoanele si logica lor
        Poate fi selectat doar un buton maxim intr-un moment
    """

    AlegeCuloarea = tk.LabelFrame(ParteaDeInceput, text = "Alege Culoarea", padx = 10, pady = 10)
    AlegeCuloarea.pack(padx = 10, pady = 10)

    """
            Aici imi voi selecta culoarea cu care voi juca
            acest lucru l-am facut prin functiile de clasa 
            care verifica daca schimbariile sunt bune
    """
    def change1():
        Joc.changeColors1()
        Rosu.config(state = "normal")
        Albastru.config(state = tk.DISABLED)
    
    def change2():
        Joc.changeColors2()
        Rosu.config(state = tk.DISABLED)
        Albastru.config(state = "normal")
        
    Rosu = tk.Button(AlegeCuloarea, command = change2, state = tk.DISABLED, text = "Vreau sa fiu rosu")
    Albastru = tk.Button(AlegeCuloarea, command = change1, text = "Vreau sa fiu albastru")
    Rosu.grid(padx = 5, pady = 5, row = 0, column = 0)
    Albastru.grid(padx = 5, pady = 5, row = 0, column = 1)
    change2() # ma asigur mereu ca am culoarea rosie de start

    AlegeAlgoritmul = tk.LabelFrame(ParteaDeInceput, text = "AlegeAlgoritmul",padx = 20, pady = 20)
    AlegeAlgoritmul.pack(pady = 5)

    def minmax():
        global algoritmul
        algoritmul = "minmax"
        MinMax.config(state = tk.DISABLED)
        AlfaBeta.config(state = "normal")
        
    def alfabeta():
        global algoritmul
        algoritmul = "alfabeta"
        MinMax.config(state = "normal")
        AlfaBeta.config(state = tk.DISABLED)

    """
        2 butoane pe baza carora am implementat o logica cand aelegem un algoritm
            a) daca alegem minmax, se va deselecta alfabea si invers
    """

    MinMax = tk.Button(AlegeAlgoritmul, text = "MinMax", command = minmax, state = tk.DISABLED)
    MinMax.grid(padx = 6)
    AlfaBeta = tk.Button(AlegeAlgoritmul, text = "AlfaBeta", command = alfabeta)
    AlfaBeta.grid(row = 0, column = 1, padx = 6)

    SeteazaNumelePlayerilor = tk.LabelFrame(ParteaDeInceput, text = "seteaza numele playerilor",padx = 20, pady = 20)
    SeteazaNumelePlayerilor.pack(pady = 5)

    def p1():
        Joc.setPlayer1Name(Player1Entry.get())
        Player1Entry.delete(0,tk.END)

    Player1Entry = tk.Entry(SeteazaNumelePlayerilor, justify = tk.CENTER)
    Player1Entry.grid(row = 0, column = 0, padx = 2, pady = 10)
    Player1Buton = tk.Button(SeteazaNumelePlayerilor, text = "Set player 1 name", command = p1)
    Player1Buton.grid(row = 0, column = 1, padx = 2, pady = 10)

    def p2():
        Joc.setPlayer2Name(Player2Entry.get())
        Player2Entry.delete(0,tk.END) 

    Player2Entry = tk.Entry(SeteazaNumelePlayerilor, justify = tk.CENTER)
    Player2Entry.grid(row = 1, column = 0, padx = 2, pady = 10)
    Player2Buton = tk.Button(SeteazaNumelePlayerilor, text = "Set player 2 name", command = p2)
    Player2Buton.grid(row = 1, column = 1, padx = 2, pady = 10)

    AlegeDificultate = tk.LabelFrame(ParteaDeInceput, padx = 10, pady = 10, text = "Alegere dificultatea")
    AlegeDificultate.pack(padx = 10, pady = 10)

    """
        Alegerea dificultatii am facut-o prin intermediul a 3 butaone 
        fiecare buton e specific unei dificultati anume:
            a) Easy
            b) Mediu
            c) Hard
    """

    def easy():#imi setez dificultatea cea mai usoara, adica adancimea arborelui meu in cadrul algoritmilor mei este 1
        global dificultate
        dificultate = 0
        Medium.config(state = "normal")
        Easy.config(state = tk.DISABLED)
        Hard.config(state = "normal")

    Easy = tk.Button(AlegeDificultate, text = "Easy", command = easy, state = tk.DISABLED)
    Easy.grid(row = 0, column = 0, padx = 4, pady = 5)

    def medium():#imi setez dificultatea medie, adica adancimea arborelui meu in cadrul algoritmilor mei este 2
        global dificultate
        dificultate = 1
        Medium.config(state = tk.DISABLED)
        Easy.config(state = "normal")
        Hard.config(state = "normal")

    Medium = tk.Button(AlegeDificultate, text = "Mediu", command = medium)
    Medium.grid(row = 0, column = 1, padx = 4, pady = 5)

    def hard(): #imi setez dificultatea cea mai mare, adica adancimea arborelui meu in cadrul algoritmilor mei este 3
        global dificultate
        dificultate = 2
        Medium.config(state = "normal")
        Easy.config(state = "normal")
        Hard.config(state = tk.DISABLED)

    Hard = tk.Button(AlegeDificultate, text = "Hard", command = hard)
    Hard.grid(row = 0, column = 2, padx = 4, pady = 5)

    def start():
        ParteaDeInceput.destroy() # sterg partea de inceput pentru a imi creea tabla de joc
        ParteaDeJoc = tk.Frame(root,padx = 10, pady = 10)
        ParteaDeJoc.pack()
        makeJoc() # aceasta functie imi va creea jocul

    
    IncepeJoc = tk.Button(ParteaDeInceput, text = "Joaca", command = start)
    IncepeJoc.pack()

meniu()

root.mainloop()