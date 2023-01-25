ROUND = 12
D = 8 # albo 8 xD
S = 4
ReductionPoly = 0x3
WORDFILTER = (1 << S) - 1

RC = [
    [1, 3, 7, 14, 13, 11, 6, 12, 9, 2, 5, 10],
    [0, 2, 6, 15, 12, 10, 7, 13, 8, 3, 4, 11],
    [2, 0, 4, 13, 14, 8, 5, 15, 10, 1, 6, 9],
    [6, 4, 0, 9, 10, 12, 1, 11, 14, 5, 2, 13],
    [14, 12, 8, 1, 2, 4, 9, 3, 6, 13, 10, 5],
    [15, 13, 9, 0, 3, 5, 8, 2, 7, 12, 11, 4],
    [13, 15, 11, 2, 1, 7, 10, 0, 5, 14, 9, 6],
    [9, 11, 15, 6, 5, 3, 14, 4, 1, 10, 13, 2]
]

MixColMatrix= [
	[ 2,  4,  2, 11,  2,  8,  5,  6],
	[12,  9,  8, 13,  7,  7,  5,  2],
	[ 4,  4, 13, 13,  9,  4, 13,  9],
	[ 1,  6,  5,  1, 12, 13, 15, 14],
	[15, 12,  9, 13, 14,  5, 14, 13],
	[ 9, 14,  5, 15,  4, 12,  9,  6],
	[12,  2,  2, 10,  3,  1,  1, 14],
	[15,  1, 13, 10,  5, 10,  2,  3]
]

m_8_matrix = [ 
    [2,4,2,11  , 2  , 8  , 5  , 6], 
    [12,26  , 16  , 68  , 23  , 50  , 38  , 41] ,
    [82,176,108 , 467  , 150  , 351  , 255  , 284] ,
    [568 , 1218 , 744  , 3232 , 1035 , 2422 , 1771 , 1959] ,
    [3918 , 8404 , 5136 , 22293 , 7150 , 16707 , 12217 , 13525] ,
    [27050 , 58018 , 35454 , 153911 , 49343 , 115350 , 84332 , 93367] ,
    [186734 , 400518 , 244752 , 1062491 , 340645 , 796279 , 582185 , 644534] ,
    [1289068, 2764870 , 1689586 , 7334626 , 2351559 , 5496917 , 4018949 , 4449389]
]

sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]


def selectConst(condition1,condition2,opt1,opt2,opt3,opt4):
    if (condition1 and condition2):
        return opt1
    elif(condition1):
        return opt2
    elif(condition2):
        return opt3
    else:
        return opt4

def AddKey(state, round):
    for i in range(D):
        state[i][0] ^= RC[i][round]
    return state

def SubCell(state):
    for i in range(D):
        for j in range(D):
            state[i][j] = sbox[state[i][j]]
    return state

def ShiftRow(state):
    for i in range(1, D):
        tmp = [0]*D
        for j in range(D):
            tmp[j] = state[i][j]
        for j in range(D):
            state[i][j] = tmp[(j+i)%D]
    return state
def FieldMult(a, b):
    x = a
    ret = 0
    for i in range(S):
        if (b >> i) & 1:
            ret ^= x
        if (x >> (S - 1)) & 1:
            x <<= 1
            x ^= ReductionPoly
        else:
            x <<= 1
    return ret & WORDFILTER

def myMixColumn(state):
    for i in range(D):
        for j in range(D):
            state[i][j] = state[i][j] & m_8_matrix[i][j]
    return state

def MixColumn(state):
    for j in range(D):
        tmp = [0]*D
        for i in range(D):
            sum = 0
            for k in range(D):
                sum ^= FieldMult(MixColMatrix[i][k], state[k][j])
            tmp[i] = sum
        for i in range(D):
            state[i][j] = tmp[i]
    return state

def printState(state):
    print("------------------------")
    for i in state:
        for j in i:
            print(hex(j),end=' ')
        print()
    

def Permutation(state, r):
    for i in range(r):
        print(i,"############################")
        # if DEBUG:
        #     print("--- Round %d ---" % i)
        state = AddKey(state, i)
        printState(state)
        state = SubCell(state)
        printState(state)
        state = ShiftRow(state)
        printState(state)
        state = MixColumn(state)
        printState(state)
    return state











inputData = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 8, 2, 0, 2, 0]
]

if __name__ == "__main__":
    # inputData = []
    # for i in range(7):
    #     inputData.append([0,0,0,0,0,0,0,0])
    # inputData.append([0,0,0,15,7,7,0,0])

    Permutation(inputData,12)