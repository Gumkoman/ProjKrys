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

def gen_tag(state: bytes, OUT: int):
    tag = ''
    # if OUT == 16:
    #     assert OUT == 16, "Must compute 128-bit tag !"
    #     photon256(state)
    #     tag[:OUT] = state[:OUT]
    # else:
    assert OUT == 32, "Must compute 256-bit tag !"
    state = Permutation(state)
    tag[:OUT//2] = state[:OUT//2]
    state = Permutation(state)
    tag[OUT//2:] = state[:OUT//2]
    return tag



def binaryAddition(a,b):
    return bin(int(a, 2) + int(b, 2))

def photon_betle_Hash(M,r):
    if len(M) == 0:
        iv = b'0'+b'0'
        T = gen_tag(binaryAddition(iv,1),256)
        return T, iv
    elif len(M) <= 128:   # 128 bitów albo mniej
        c0 = 1 if len(M) < 128 else 2
        iv = Ozs(M)+b'0'
        iv = Ozs(M,128)+b'0'
        T = gen_tag(binaryAddition(iv , c0),256)
        return T, iv
        pass
    else:
        M1, M2 = (M[:128], M[128:])
        c0 = 1 if (len(M2)%r) else 2
        iv = M1 + b'0'
        iv = HASH(r,iv,M2,c0)
        T = gen_tag(iv,256)
        return T, iv

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
    print(photon_betle_Hash('',1))