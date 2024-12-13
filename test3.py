from src import lynxy
from rich import print
from ast import literal_eval

inst = lynxy.Lynxy()
message = 'hi'
encrypted = inst.comm.sec.RSA_encrypt(message, True)
padded = inst.comm.parser.addPadding(encrypted)
unpadded = inst.comm.parser.removePadding(padded)
elem = unpadded[0]
# print(type(elem))
# print(elem)
new = literal_eval(elem)
# print(type(new))
# print(new)
decrypted = inst.comm.sec.RSA_decrypt(new)
print(decrypted)