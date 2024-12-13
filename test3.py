from src import lynxy
from rich import print
from ast import literal_eval

inst = lynxy.Lynxy()
message = 'hi'
encrypted = inst.comm.sec.RSA_encrypt(message, True)
padded = inst.comm.parser.addPadding(encrypted)
unpadded = inst.comm.parser.removePadding(padded)
elem = unpadded[0]
decrypted = inst.comm.sec.RSA_decrypt(elem)
print(decrypted)