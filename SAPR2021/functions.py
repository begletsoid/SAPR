import numpy
import matplotlib as ptl
from numpy import linalg
def generateReactionsMatrix(kernels, left, right):
    count = len(kernels)
    A = numpy.zeros((count+1, count+1), dtype=int).tolist()
    for i in range(count):
        A[i][i] += kernels[i].A*kernels[i].materialObj.elasticity/kernels[i].L
        A[i][i+1] -= kernels[i].A*kernels[i].materialObj.elasticity/kernels[i].L
        A[i+1][i] -= kernels[i].A*kernels[i].materialObj.elasticity/kernels[i].L
        A[i+1][i+1] += kernels[i].A*kernels[i].materialObj.elasticity/kernels[i].L
    if left == True:
        A[0][0] = 1
        A[1][0] = 0
        A[0][1] = 0
    if right == True:
        A[count][count] = 1
        A[count-1][count] = 0
        A[count][count-1] = 0
    print('Reaction Matrix', A)
    return A

def generateReactionsGlobalVector(kernels, concentrateds, left, right):
    count = len(kernels)
    knots = [0] * (count+1)
    for conc in concentrateds:
        knots[conc.point-1] = conc.power
    print('knots', knots)
    for kern in kernels:
        print('running', kern.Q)
    B = [0] * (count+1)
    for i in range(count+1):
        B[i] += knots[i]
        if i != 0:
            B[i] += kernels[i-1].Q * kernels[i-1].L/2
        if i != count:
            B[i] += kernels[i].Q * kernels[i].L/2
    if left == True:
        B[0] = 0
    if right == True:
        B[count] = 0
    print('Reaction Global Vector', B)
    return B

def generateDeltas(kernels, concentrateds, left, right):
    count = len(kernels)
    A = generateReactionsMatrix(kernels, left, right)
    B = generateReactionsGlobalVector(kernels, concentrateds, left, right)
    try:
        A = linalg.inv(A)
    except:
        linalg.lstsq(A, A)
    ans = numpy.dot(A,B)
    print('Deltas', ans)
    return ans

def solveN(kernels, concentrateds, left, right):
    count = len(kernels)
    A = generateReactionsMatrix(kernels, left, right)
    B = generateReactionsGlobalVector(kernels, concentrateds, left, right)
    try:
        A = linalg.inv(A)
    except:
        linalg.lstsq(A, A)
    v6 = numpy.dot(A,B)
    N  = numpy.zeros((count, 2), dtype=int).tolist()
    for i in range(count):
        N[i][0] = (kernels[i].A * kernels[i].materialObj.elasticity/kernels[i].L) * (v6[i+1] -v6[i])
        if kernels[i].Q != 0:
            N[i][0] += (kernels[i].Q * kernels[i].L / 2)
            N[i][1] -= kernels[i].Q #* kernels[i].L
    print('N', N)
    return N

def solveU(kernels, concentrateds, left, right):
    count = len(kernels)
    A = generateReactionsMatrix(kernels, left, right)
    B = generateReactionsGlobalVector(kernels, concentrateds, left, right)
    try:
        A = linalg.inv(A)
    except:
        linalg.lstsq(A, A)
    v6 = numpy.dot(A,B)
    U = numpy.zeros((count, 3), dtype=int).tolist()
    for i in range(count):
        U[i][0] = v6[i]
        U[i][1] = (v6[i+1] - v6[i]) / kernels[i].L
        U[i][1] += (kernels[i].Q * kernels[i].L) / (2 * kernels[i].materialObj.E * kernels[i].A)
        U[i][2] = -(kernels[i].Q / (2*kernels[i].materialObj.E * kernels[i].A))
    print('U', U)
    return U