from src.lynxy import Lynxy
from rich import print
import random
import datetime

inst = Lynxy()
def recv(data):
    unpad = inst._comm.parser.removePadding(data)
    for dat in unpad:
        dec = inst._comm.sec.RSA_decrypt(dat)
        print('dec:', dec)
while True:
    current = datetime.datetime.strftime(datetime.datetime.now(), "%d/%m/%Y, %H:%M:%S")
    encrypted = inst._comm.sec.RSA_encrypt(current, True)
    padded = inst._comm.parser.addPadding(encrypted)
    # print('original:', padded)
    while padded:
        randNum = random.randint(0, len(padded))
        chars = padded[:randNum]
        padded = padded.removeprefix(chars)
        # print('current:', padded)
        # print('selected chars:', chars)
        recv(chars)