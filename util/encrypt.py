import os
import sys
import base64
from dotenv import load_dotenv, find_dotenv
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


load_dotenv(find_dotenv('config.env'))

password = os.environ['RH_PASSWORD'].encode('UTF-8')
salt = os.environ['SALT'].encode('UTF-8')
filename = os.environ.get('FILE') or sys.argv[1]

kdf = Scrypt(
    salt=salt,
    length=32,
    n=2**14,
    r=8,
    p=1,
)

key = base64.urlsafe_b64encode(kdf.derive(password))
f = Fernet(key)
with open(filename, 'r') as file:
    ciphertext = f.encrypt(file.read().encode('UTF-8'))

with open(f'{filename}.encrypted', 'wb') as file:
    file.write(ciphertext)
