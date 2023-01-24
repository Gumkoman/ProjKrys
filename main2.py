import struct
import sys

NONCE_LEN = 16
KEY_LEN = 16

RATE = 4 # RATE is in terms of bytes, allowed values are {4, 16}.


#check with specification
def encrypt_Photon_AEAD(encryption_key,nonce,data,message):
    ciphertext = ''
    tag = ''
    plaintext = '' # type bytearray or string ?
    state = bytearray(32)

    state[0:NONCE_LEN] = nonce[0:NONCE_LEN]
    state[NONCE_LEN:NONCE_LEN+KEY_LEN] = encryption_key[0:KEY_LEN]

    if (len(data) == 0) and (len(encryption_key) == 0):
        state[31] ^= (1 << 5)
        gen_tag(state,tag)
        return
    
    f0 = len(encryption_key) > 0
    f1 = (len(data) & (RATE - 1)) == 0
    f2 = len(data) > 0
    f3 = (len(encryption_key) & (RATE - 1)) == 0

    C0 = 1 if (f0 and f1) else 2 if f0 else 3 if f1 else 4
    C1 = 1 if (f2 and f3) else 2 if f2 else 5 if f3 else 6

    if len(data) > 0:
        absorb(state, data, len(data), C0)
        
    
    if len(encryption_key) > 0:
        for off in range(0, len(encryption_key), RATE):
            photon256(state)
            len_ = min(RATE, len(encryption_key) - off)
            # inv_rho(state, encryption_key[off:off+len], plaintext[off:off+len], len_)
    state[31] ^= (C1 << 5)

    gen_tag(state, tag)
    return ciphertext,tag

OUT = 16

#check with specification
def gen_tag(state, tag):
    if OUT == 16:
        assert OUT == 16, "Must compute 128 -bit tag !"
        photon256(state)
        tag[:OUT] = state[:OUT]
    else:
        assert OUT == 32, "Must compute 256 -bit tag !"
        photon256(state)
        tag[:OUT//2] = state[:OUT//2]
        photon256(state)
        tag[OUT//2:] = state[:OUT//2]

#check with specification
def absorb(state, msg, mlen, C, RATE = 4):
    if RATE == 4:
        assert RATE == 4, "Rate portion of state must be 32 -bit wide"
        full_blk_cnt = mlen // RATE
        full_blk_bytes = full_blk_cnt * RATE
        off = 0
        while off < full_blk_bytes:
            photon256(state)
            rate = struct.unpack("<I", state[:RATE])[0]
            mword = struct.unpack("<I", msg[off:off+RATE])[0]
            nrate = rate ^ mword
            struct.pack_into("<I", state, 0, nrate)
            off += RATE
        rm_bytes = mlen - off
        if rm_bytes > 0:
            photon256(state)
            rate = struct.unpack("<I", state[:RATE])[0]
            if sys.byteorder == "little":
                mword = (1 << (rm_bytes * 8)) & 0xffffffff
                struct.pack_into("<I", mword, 0, msg[off:off+rm_bytes])
                nrate = rate ^ mword
                struct.pack_into("<I", state, 0, nrate)
            else:
                mword = (16777216 >> (rm_bytes * 8)) & 0xffffffff
                struct.pack_into("<I", mword, 0, msg[off:off+rm_bytes])
                nrate = rate ^ mword
                struct.pack_into("<I", state, 0, nrate)

ROUNDS = 11

S_Box = ['C', '5', '6', 'B', '9', '0', 'A', 'D', '3', 'E', 'F', '8', '4', '7', '1', '2']

def SubCells(X):
    for i in range(8):
        for j in range(8):
            X[i][j] = S_Box(X[i][j])
    return X

def ShiftRows(X):
    X_ = [[0 for _ in range(8)] for _ in range(8)]
    for i in range(8):
        for j in range(8):
            X_[i][j] = X[i][(j + i) % 8]
    return X_



def add_constant(X,k):
    RC = [1, 3, 7, 14, 13, 11, 6, 12, 9, 2, 5, 10]
    IC = [0, 1, 3, 7, 15, 14, 12, 8]
    for i in range(8):
        X[i, 0] = X[i, 0] ^ RC[k] ^ IC[i]
    return X

def mix_column_serial(X):
    M = [2, 4, 2, 11, 2, 8, 5, 6]
    M_ = []
    for i in range(8):
        M_.append(M)
    for i in range(8):
        for j in range(8):
            X[i][j] = X[i][j] & M_[i][j]
    return X
    

def photon256(state):
    for i in range(ROUNDS):
        state = add_constant(state, i)
        state = SubCells(state)
        state = ShiftRows(state)
        state = mix_column_serial(state)


if __name__ == "__main__":
    mix_column_serial(1)

