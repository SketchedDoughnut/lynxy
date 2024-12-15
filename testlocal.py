from src import lynxy
from rich import print
from ast import literal_eval

inst = lynxy.Lynxy()
data = 'test!'
encrypted = inst.comm.sec.RSA_encrypt(data, True)
padded = inst.comm.parser.addPadding(encrypted)
# print(padded)

split = padded.split(inst.comm.parser.byteEndMarker)
# print('split:', split)
if len(split[-1]) == 0: split.pop(-1)
for elem in split:
    print(inst.comm.sec.RSA_decrypt(elem))