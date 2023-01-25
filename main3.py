import struct
ROUND = 12
D = 8 # albo 8 xD
S = 4
ReductionPoly = 0x3
WORDFILTER = (1 << S) - 1
import permutation

# RC = [
#     [1, 3, 7, 14, 13, 11, 6, 12, 9, 2, 5, 10],
#     [0, 2, 6, 15, 12, 10, 7, 13, 8, 3, 4, 11],
#     [2, 0, 4, 13, 14, 8, 5, 15, 10, 1, 6, 9],
#     [6, 4, 0, 9, 10, 12, 1, 11, 14, 5, 2, 13],
#     [14, 12, 8, 1, 2, 4, 9, 3, 6, 13, 10, 5],
#     [15, 13, 9, 0, 3, 5, 8, 2, 7, 12, 11, 4],
#     [13, 15, 11, 2, 1, 7, 10, 0, 5, 14, 9, 6],
#     [9, 11, 15, 6, 5, 3, 14, 4, 1, 10, 13, 2]
# ]

# MixColMatrix= [
# 	[ 2,  4,  2, 11,  2,  8,  5,  6],
# 	[12,  9,  8, 13,  7,  7,  5,  2],
# 	[ 4,  4, 13, 13,  9,  4, 13,  9],
# 	[ 1,  6,  5,  1, 12, 13, 15, 14],
# 	[15, 12,  9, 13, 14,  5, 14, 13],
# 	[ 9, 14,  5, 15,  4, 12,  9,  6],
# 	[12,  2,  2, 10,  3,  1,  1, 14],
# 	[15,  1, 13, 10,  5, 10,  2,  3]
# ]

# m_8_matrix = [ 
#     [2,4,2,11  , 2  , 8  , 5  , 6], 
#     [12,26  , 16  , 68  , 23  , 50  , 38  , 41] ,
#     [82,176,108 , 467  , 150  , 351  , 255  , 284] ,
#     [568 , 1218 , 744  , 3232 , 1035 , 2422 , 1771 , 1959] ,
#     [3918 , 8404 , 5136 , 22293 , 7150 , 16707 , 12217 , 13525] ,
#     [27050 , 58018 , 35454 , 153911 , 49343 , 115350 , 84332 , 93367] ,
#     [186734 , 400518 , 244752 , 1062491 , 340645 , 796279 , 582185 , 644534] ,
#     [1289068, 2764870 , 1689586 , 7334626 , 2351559 , 5496917 , 4018949 , 4449389]
# ]

# sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]


# def selectConst(condition1,condition2,opt1,opt2,opt3,opt4):
#     if (condition1 and condition2):
#         return opt1
#     elif(condition1):
#         return opt2
#     elif(condition2):
#         return opt3
#     else:
#         return opt4

# def AddKey(state, round):
#     for i in range(D):
#         state[i][0] ^= RC[i][round]
#     return state

# def SubCell(state):
#     for i in range(D):
#         for j in range(D):
#             state[i][j] = sbox[state[i][j]]
#     return state

# def ShiftRow(state):
#     for i in range(1, D):
#         tmp = [0]*D
#         for j in range(D):
#             tmp[j] = state[i][j]
#         for j in range(D):
#             state[i][j] = tmp[(j+i)%D]
#     return state
# def FieldMult(a, b):
#     x = a
#     ret = 0
#     for i in range(S):
#         if (b >> i) & 1:
#             ret ^= x
#         if (x >> (S - 1)) & 1:
#             x <<= 1
#             x ^= ReductionPoly
#         else:
#             x <<= 1
#     return ret & WORDFILTER

# def myMixColumn(state):
#     for i in range(D):
#         for j in range(D):
#             state[i][j] = state[i][j] & m_8_matrix[i][j]
#     return state

# def MixColumn(state):
#     for j in range(D):
#         tmp = [0]*D
#         for i in range(D):
#             sum = 0
#             for k in range(D):
#                 sum ^= FieldMult(MixColMatrix[i][k], state[k][j])
#             tmp[i] = sum
#         for i in range(D):
#             state[i][j] = tmp[i]
#     return state

# def printState(state):
#     print("------------------------")
#     for i in state:
#         for j in i:
#             print(hex(j),end=' ')
#         print()
    

# def Permutation(state, r):
#     for i in range(r):
#         print(i,"############################")
#         # if DEBUG:
#         #     print("--- Round %d ---" % i)
#         state = AddKey(state, i)
#         printState(state)
#         state = SubCell(state)
#         printState(state)
#         state = ShiftRow(state)
#         printState(state)
#         state = MixColumn(state)
#         printState(state)
#         # for state_ in state:
#         #     print(state_)



def PHOTON_Permutation(State_in):
    state = [[0 for _ in range(D)] for _ in range(D)]

    for i in range(D * D):
        state[i // D][i % D] = (State_in[i // 2] >> (4 * (i & 1))) & 0xf

    state = Permutation(state, ROUND)

    State_in = bytearray((D * D) // 2)
    for i in range(D * D):
        State_in[i // 2] |= (state[i // D][i % D] & 0xf) << (4 * (i & 1))


def ENCorDEC(State_inout, Data_out, Data_in, Dlen_inbytes, Constant, EncDecInd):
    State = State_inout
    Dlen_inblocks = (Dlen_inbytes + RATE_INBYTES - 1) // RATE_INBYTES
    LastDBlocklen = 0
    i = 0

    for i in range(Dlen_inblocks - 1):
        State = PHOTON_Permutation(State)
        Data_out[i * RATE_INBYTES : (i + 1) * RATE_INBYTES] = rhoohr(State, Data_in[i * RATE_INBYTES : (i + 1) * RATE_INBYTES], RATE_INBYTES, EncDecInd)

    State = PHOTON_Permutation(State)
    LastDBlocklen = Dlen_inbytes - i * RATE_INBYTES
    Data_out[i * RATE_INBYTES : (i + 1) * RATE_INBYTES] = rhoohr(State, Data_in[i * RATE_INBYTES : (i + 1) * RATE_INBYTES], LastDBlocklen, EncDecInd)
    if LastDBlocklen < RATE_INBYTES:
        State[LastDBlocklen] ^= 0x01

    State = XOR_const(State, Constant)


def crypto_aead_encrypt(c, clen, m, mlen, ad, adlen, nsec, npub, k):
    C = c
    T = c[mlen:]
    M = m
    A = ad
    N = npub
    K = k

    State = bytearray(STATE_INBYTES)
    c0 = 0
    c1 = 0

    State = N + K
    if adlen == 0 and mlen == 0:
        State[0] ^= 1
        T = struct.pack("%dB" % TAG_INBYTES, *State)
        clen[0] = TAG_INBYTES
        return 0

    c0 = selectConst((mlen != 0), ((adlen % RATE_INBYTES) == 0), 1, 2, 3, 4)
    c1 = selectConst((adlen != 0), ((mlen % RATE_INBYTES) == 0), 1, 2, 5, 6)

    if adlen != 0:
        State = HASH(State, A, adlen, c0)
    if mlen != 0:
        C = ENCorDEC(State, C, M, mlen, c1, ENC)

    T = struct.pack("%dB" % TAG_INBYTES, *State)
    clen[0] = mlen + TAG_INBYTES
    return 0

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
    permutation.Permutation(inputData,12)