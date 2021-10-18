import os
from dotenv import load_dotenv, find_dotenv
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


load_dotenv(find_dotenv('config.env'))

password = os.environ['RH_PASSWORD'].encode('UTF-8')
salt = os.environ['SALT'].encode('UTF-8')

kdf = Scrypt(
    salt=salt,
    length=32,
    n=2**14,
    r=8,
    p=1,
)

key = kdf.derive(password)
iv = salt + salt

cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
encryptor = cipher.encryptor()
ct = encryptor.update(b"a secret message") + encryptor.finalize()
decryptor = cipher.decryptor()
print(decryptor.update(ct) + decryptor.finalize())
