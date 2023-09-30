EPSILON = 0.000001
from random import choice

def determinant(A,B,C):
    """
        | 1  1   1  |
        | xa xb  xc | -> acesta este determinanutl pe care dorim sa l calculam
        | ya yb  yc |
    """

    res = 0
    res += (B[0]*C[1] - C[0]*B[1])
    res -= (A[0]*C[1] - C[0]*A[1])
    res += (A[0]*B[1] - B[0]*A[1])
    
    return res

def getPos(A,B,C):
    det = determinant(A,B,C)
    if abs(det) < EPSILON:
        return 0
    elif det < 0:
        return -1 # in dreapta
    else:
        return 1 # in stange

def anl(A,B,C):
    val = getPos(A,B,C)
    if val < 0:
        print("Rotatie dreapta")
    if val == 0:
        print("Coliniare")
    if val > 0:
        print("Rotatie stanga")

A = (0,0)
B = (1,1)
C = (1,0)
anl(A,C,B)

def getLeftPoint(P):
    mini = None
    for i in P:
        if mini == None:
            mini = i
        else:
            if mini[0] > i[0]:
                mini = i
            elif mini[0] == i[0] and mini[1] > i[1]:
                mini = i
    return mini

def Jarvis(P):
    L = []
    n = len(P)
    k = 0
    L.append(getLeftPoint(P))
    while True:
        S = P[choice([i for i in range(n)])]
        while S == L[k]:
            S = P[choice([i for i in range(n)])] 

        for i in P:
            if getPos(L[k],S,i) < 0 and i != L[k]:
                S = i
        if S == L[0]:
            break
        k += 1
        L.append(S)
    return L

nrPuncte = int(input())
P =[tuple(map(float,input().split())) for i in range(nrPuncte)]
print(*Jarvis(P))
