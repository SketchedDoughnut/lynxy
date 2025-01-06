'''
This is the sec file, which contains all of the encryption tools. There are functions for both encryption and decryption
for RSA and Fernet (AES with a 128 bit key). RSA is only used for exchanging Fernet keys when the two machines
connect to each other.
'''

# included modules
import pickle

# external modules
import rsa
from cryptography.fernet import Fernet

# files
from .exceptions import Exceptions

####################################################

# the main class for managing
# security layers
class Sec:
    def __init__(self):
        ############## 
        # FOR RSA ENCRYPTION
        # AKA ASYMMETRICAL
        ##############
        # represents internal public and private keys
        # for this end of communication
        self.int_pub_key, self.int_priv_key = self._gen_access_keys()
        # represents the external public key, we don't get their private key
        # for other end of communication
        self.ext_pub_key = None
        ##############
        # FOR FERNET ENCRYPTION
        # AKA SYMMETRICAL
        ##############
        # represents the main fernet object and key
        # this manager by default starts off with its own encryption key and tool
        self.fernet_key = Fernet.generate_key()
        self.fernet_tool = Fernet(self.fernet_key)

    
    # generates public/private keys for encryption
    def _gen_access_keys(self) -> tuple[rsa.PublicKey, rsa.PrivateKey]: return rsa.newkeys(1024)


    # function that loads RSA public key
    def load_RSA(self, ext_pub_key: rsa.PublicKey) -> None: self.ext_pub_key = ext_pub_key


    # function that loads Fernet key
    def load_Fernet(self, fernet_key: bytes) -> None: 
        self.fernet_key = fernet_key
        self.fernet_tool = Fernet(self.fernet_key)
        return None


    # function that encrypts using RSA and a public key
    def RSA_encrypt(self, data: any, use_internal: bool = False) -> bytes:
        # if use_internal, then we use int_pub_key to encrypt
        # otherwise we use ext_pub_key
        if use_internal: activeKey = self.int_pub_key
        else: activeKey = self.ext_pub_key
        if activeKey == None: raise Exceptions.NoExteralPublicKeyError()
        pickledData = pickle.dumps(data)
        encryptedData = rsa.encrypt(pickledData, activeKey)
        return encryptedData


    # function that decrypts using RSA and a private key
    def RSA_decrypt(self, data: bytes) -> any:
        decryptedData = rsa.decrypt(data, self.int_priv_key)
        unpickledData = pickle.loads(decryptedData)
        return unpickledData
    

    # function that encrypts using Fernet and a key
    def Fernet_encrypt(self, data: any) -> bytes:
        pickledData = pickle.dumps(data)
        encryptedData = self.fernet_tool.encrypt(pickledData)
        return encryptedData
    

    # function that decrypts using Fernet and a key
    def Fernet_decrypt(self, data: bytes) -> any:
        decryptedData = self.fernet_tool.decrypt(data)
        unpickledData = pickle.loads(decryptedData)
        return unpickledData