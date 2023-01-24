

def concatenate(ouput, left,leftLen, right,rightLen):
    return left[:leftLen]+right[:rightLen]
    

def cryptoAeadDecrypt(c,clen,m,mlen,ad,adlen,nsec,npub,k):
    State = ''
    State = concatenate(State,npub,NOUNCE_INBYTES,key,KEY_INBYTES)
    print(State)


def cryptoAeadEncrypt():
    pass

CRYPTO_NPUBBYTES = 16
NOUNCE_INBYTES = 16

CRYPTO_KEYBYTES = 16
KEY_INBYTES = 16


CRYPTO_BYTES = 64

if __name__ == "__main__":
    
    mlen = 0
    clen = 0
    plaintext = 'hello'
    cipher = ''
    key = '0123456789ABCDEF0123456789ABCDEF'
    nonce = '000000000000111111111111'
    ad = ''
    nsec = ''
    npub = ''

    print('PHOTON-BETTLE AEAD light-wight cipher')
    print('Plain text:',plaintext)
    print('Key:',key)
    print("Nonce:",nonce)
    print("Aditionall information:",ad)

    ret = cryptoAeadDecrypt(cipher,clen,plaintext,len(plaintext),ad,len(ad),nsec,npub,key)