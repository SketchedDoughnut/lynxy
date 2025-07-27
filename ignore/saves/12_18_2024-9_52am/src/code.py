# TODO
# temporary recieving function
def _recv(self) -> None:
    while True:
        # recieve how many bytes message is
        recievedNetworkOrder = self.TCP_client.recv(1024)
        if recievedNetworkOrder is None: continue # if empty ("b''")
        unpickledNetworkByteOrder = pickle.loads(recievedNetworkOrder)
        targetByteCount = socket.ntohl(unpickledNetworkByteOrder)
        # recieve byteCount amount of bytes of data
        # we load leftover to continue where it left off
        recievedData = self.parser.carry

        print('starting with:', recievedData)

        while True:
            recievedData += self.TCP_client.recv(targetByteCount)
            # ensure full data recieved
            intData = int.from_bytes(recievedData)
            recievedByteCount = intData.bit_length()

            print(f'{recievedByteCount}, {targetByteCount}, {recievedData}')

            if recievedByteCount >= targetByteCount: break
        # remove padding
        unpaddedData = self.parser.removePadding(recievedData)
        # decrypt each part
        for indivData in unpaddedData:
            print(f'decrypting ({unpaddedData.index(indivData)}):', indivData)
            decryptedData = self.sec.RSA_decrypt(indivData)
            print(f'recv ({unpaddedData.index(indivData)}):', decryptedData)
            self._trigger(Constants.Event.ON_MESSAGE, decryptedData)


# TODO
# this function sends data to the other machine
def _send(self, data: any, ignore_errors: bool = False) -> None:
    # raise error message if data is empty
    # and raise is toggled, otherwise return
    raiseError = False
    if len(data) == 0: raiseError = True
    if data is None: raiseError = True
    if not ignore_errors and raiseError: raise Exceptions.EmptyDataError()
    if ignore_errors and raiseError: return
    # find how many bytes encrypted data is
    encryptedData = self.sec.RSA_encrypt(data) # encrypt data
    paddedData = self.parser.addPadding(encryptedData) # pad data
    intData = int.from_bytes(paddedData) # get int of encoded data
    byteCount = intData.bit_length() # how many bits it takes to represent our int
    networkByteOrder = socket.htonl(byteCount) # convert to network (universal) order
    self.TCP_client.sendall(pickle.dumps(networkByteOrder)) # send length
    self.TCP_client.sendall(paddedData) # send actual data
    return