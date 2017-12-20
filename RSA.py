
__author__ = 'davidwer'
from binascii import unhexlify
from math import gcd
import gmpy2
import itertools

files = []
modulus = []
message = []
p_and_q = []
e = 65537

# List with name of the files
with open("intercepted/int.txt", 'r') as f:
    for i in range(100):
        files.append(f.readline().rstrip("\n\r"))  # Remove \n from file name

# Loop opening all files and reading from them
for f in files:
    with open("intercepted/" + f, 'r') as m:
        fil = m.read()
        modulus.append(int(fil[fil.index(' ')+1:fil.index('S')], 16))  # Add modulus to list
        message.append(int(fil[fil.index('S')+len("ecret Message: "):], 16))  # Add secret message to list
# -----------------------------------------------------------------------------------------


def long_to_bytes (val, endianness='big'):
    """
    https://stackoverflow.com/questions/8730927/convert-python-long-int-to-fixed-size-byte-array
    """
    width = val.bit_length()
    width += 8 - ((width % 8) or 8)
    fmt = '%%0%dx' % (width // 4)
    s = unhexlify(fmt % val)
    if endianness == 'little':
        s = s[::-1]
    return s
# -----------------------------------------------------------------------------------------


def find_d(i):
    """
    Find the d that way qwe can calculate M^d(mod n)
    :param i: The n
    :return: Modular multiplicative inverse of e modulus (p-1)*(q-1)
    """
    for p in p_and_q:
        mod = int((p - 1) * (i//p - 1) % i)
        if i % p == 0 and mod != 0:
            return int(gmpy2.invert(e, mod))   # Modular multiplicative inverse
    return 0
# -----------------------------------------------------------------------------------------


def decrypt(i):
    """
    Decrypt and display the secret massage
    :param i: Decrypt the i massage. The value i is the n
    :return: Non
    """
    d = find_d(i)
    if d == 0: return
    m = pow(message[modulus.index(i)], d, i)  # M^d(mod n)
    string = long_to_bytes(m).decode('utf-8')
    print("Message number: ", modulus.index(i) + 1)
    print(string)
# ---------------------------------------------------------------------------------------------


def find_flag():
    """
    Run over all n's: Find primes and decrypt
    :return: Non
    """
    combinations = list((itertools.combinations(modulus, 2)))
    for i in combinations:
        p = gcd(i[0], i[1])
        if p != 1 and p not in p_and_q:
            p_and_q.append(p)
    for i in modulus:
        decrypt(i)


find_flag()
