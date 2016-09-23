

import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg



def InvMatViaSVD(A,Dump):
    U,s,W = linalg.svd(A)
    
    NbDiag = s.size  
    print("Taille Diag dans SVD: %s" %NbDiag)
    S = np.zeros((NbDiag,NbDiag),dtype = 'float')
    InvS = np.zeros((NbDiag,NbDiag),dtype = 'float')

    for i in range(0,NbDiag,1):
#        if s[i] <> 0:
        InvS[i,i]=1/s[i]
        S[i,i]=s[i]

    if Dump:
        print("USW - A")
        print(np.dot(U,np.dot(S,W))-A)
    
    InvA = np.dot(np.linalg.inv(W),np.dot(InvS,np.linalg.inv(U)))

    
    if Dump:
        print("Verif Id")
        print(np.dot(A,InvA))
    return(InvA)
    
def CalculEstimateurs(X,Y1):
    XtX = np.dot(np.transpose(X),X)
    print("Matrice XtX")
    print(XtX)
    
    InvXtX = InvMatViaSVD(XtX,False)
    print("InvXtX")
    print(InvXtX)
    
    InvXtXXt = np.dot(InvXtX,np.transpose(X))
    print("InvXtXXt")
    print(InvXtXXt)
    
    InvXtXXtY = np.dot(InvXtXXt,Y1)
    print("InvXtXXtY")
    print(InvXtXXtY)

    YEst = np.dot(X,InvXtXXtY)    
    return(InvXtXXtY, YEst,np.dot(np.transpose(YEst-Y),YEst-Y))



M = np.zeros((8,8),dtype = 'float')
Y = np.ones((8),dtype = 'float')
for i in range(0,8,1):
    M[i,i]=1
M[0,7]=1.0
print("Matrice M")
print(M)

Estimateurs, Prev, TotalErr = CalculEstimateurs(M,Y)

Somme=0
for i in range(0,8,1):
    Somme+=Estimateurs[i]
print("Somme")
print(Somme)
print("TotalErr: %2.5f" % TotalErr)
print(" ")
print(" ")




data=np.genfromtxt('winequality-white.csv', delimiter=";")
print(data.shape)
M = np.zeros((4898,11),dtype='float')
Y = np.zeros((4898),dtype = 'float')
Prev = np.zeros((4898),dtype = 'float')
Estimateurs = np.zeros((11),dtype = 'float')
for i in range(0,4898):
    Y[i]=data[i+1,11]
    for j in range(0,11):
        M[i,j]=data[i+1,j]

Estimateurs, Prev, TotalErr  = CalculEstimateurs(M,Y)
Erreurs = Prev - Y
print("TotalErr: %2.5f" % TotalErr)


