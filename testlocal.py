from src.lynxy import Lynxy
from rich import print

inst = Lynxy()

msg1 = inst._comm.sec.RSA_encrypt('test!', True)
msg2 = inst._comm.sec.RSA_encrypt('another test!', True)
msg1_pad = inst._comm.parser.addPadding(msg1)
msg2_pad = inst._comm.parser.addPadding(msg2)
# https://stackoverflow.com/questions/31358564/finding-the-length-of-first-half-of-a-string-using-string-slicing-in-python
msg1_half1 = msg1_pad[:len(msg1_pad) // 2]
msg2_half1 = msg2_pad[:len(msg2_pad) // 2]
msg1_half2 = msg1_pad[len(msg1_pad) // 2:]
msg2_half2 = msg2_pad[len(msg2_pad) // 2:]


parsed = inst._comm.parser.removePadding(msg1_pad + msg2_half1)
for ind in parsed:
    dec = inst._comm.sec.RSA_decrypt(ind)
    print('dec1:', dec)

parsed = inst._comm.parser.removePadding(inst._comm.parser.carry + msg2_half2)
for ind in parsed:
    dec = inst._comm.sec.RSA_decrypt(ind)
    print('dec2:', dec)