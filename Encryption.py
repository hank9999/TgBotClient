from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from Setting import EncryptionKey


def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)


async def encrypt(data):
    aes = AES.new(add_to_16(EncryptionKey), AES.MODE_ECB)
    encrypt_aes = aes.encrypt((pad(data.encode('utf-8'), 16)))
    encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')
    return encrypted_text


async def decrypt(data):
    aes = AES.new(add_to_16(EncryptionKey), AES.MODE_ECB)
    base64_decrypted = base64.decodebytes(data.encode(encoding='utf-8'))
    decrypted_text = unpad(aes.decrypt(base64_decrypted), 16).decode('utf-8')
    return decrypted_text
