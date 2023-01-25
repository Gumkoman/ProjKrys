import struct
ROUND = 12
D = 8 # albo 8 xD
S = 4
ReductionPoly = 0x3
WORDFILTER = (1 << S) - 1
from permutation import Permutation
# def TAG(Tag_out, State):
#     i = TAG_INBYTES
#     while i > SQUEEZE_RATE_INBYTES:
#         PHOTON_Permutation(State)
#         Tag_out[:SQUEEZE_RATE_INBYTES] = State[:SQUEEZE_RATE_INBYTES]
#         Tag_out = Tag_out[SQUEEZE_RATE_INBYTES:]
#         i -= SQUEEZE_RATE_INBYTES
#     #TODO
#     permutation.PhotonPermutation(State)
#     Tag_out[:i] = State[:i]

def translateHexTo2DMatrix(hex_):
    result = []
    hex_ = hex_[2:]
    empty = '0'*(64-len(hex_))
    hex_= empty +hex_
    for i in range(8):
        temp = []
        for j in range(8):
            temp.append(int(hex_[i*8+j],16))
        result.append(temp)
    return result

def translate2DmatrixToHex(matrix):
    result = ''
    for i in range(8):
        for j in range(8):
            result+= hex(matrix[i][j])[2:]
    return result

def gen_tag(state, OUT):
    tag = ''
    # print(state,type(state),OUT,type(OUT))
    # if OUT == 16:
    #     assert OUT == 16, "Must compute 128-bit tag !"
    #     photon256(state)
    #     tag[:OUT] = state[:OUT]
    # else:
    assert OUT == 32, "Must compute 256-bit tag !"
    state = Permutation(state)
    state = translate2DmatrixToHex(state)
    # tag[:OUT//2] = state[:OUT//2]
    tag += state[:OUT//2]
    state = translateHexTo2DMatrix(state)
    state = Permutation(state)
    state = translate2DmatrixToHex(state)
    # tag[OUT//2:] = state[:OUT//2]
    tag += state[:OUT//2]
    return tag



def binaryAddition(a,b):
    return hex(int(a[2:], 2) + int(b[2:], 2))

def photon_betle_Hash(M,r):
    # if len(M) == 0:
    print(M)
    if M[2] == '0':
        iv = hex(0+0)
        # T = gen_tag(binaryAddition(iv),hex(1)),32)
        T = gen_tag(translateHexTo2DMatrix(binaryAddition(iv,hex(1))),32)
        return T
    elif len(M) <= 30:   # 128 bitów albo mniej
        c0 = 1 if len(M) < 128 else 2
        iv = Ozs(M)+b'0'
        iv = Ozs(M,128)+b'0'
        T = gen_tag(binaryAddition(iv , c0),32)
        return T
    else:
        M1, M2 = (M[:128], M[128:])
        c0 = 1 if (len(M2)%r) else 2
        iv = M1 + b'0'
        iv = HASH(r,iv,M2,c0)
        T = gen_tag(iv,256)
        return T

def HASH(iv,D,c0):
    r = 32
    D = Ozs(D,32)
    d_table = []
    for i in range(len(D)//32):
        if (i+1)*32 < len(D):
            d_table.append(D[i*32:(i+1)*32])
        else:
            d_table.append(D[i*32:])
    
    for i in range(len(d_table)):
        ph = Permutation(iv)
        Y,Z = (ph[:32], ph[32:])
        W = binaryAddition(Y,d_table[i])
        iv = W+Z
    iv = binaryAddition(iv,c0)
    return iv

def Ozs(V: bytes, r: int) -> bytes:
    if len(V)*8 < r:
        padding = b'1' + (b'0' * (r - len(V)*8 - 1))
        return V + padding
    else:
        return V

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
    # permutation.Permutation(inputData,12)
    # print(photon_betle_Hash('',1))
    
    inputData = hex(258)
    inputData = hex(0)
    print(type(inputData),inputData,len(inputData)-2)
    t = photon_betle_Hash(inputData,32)
    print(t)