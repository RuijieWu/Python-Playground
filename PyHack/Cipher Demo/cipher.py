'''
Hybrid Cryptor Demo
'''
from Cryptodome.Cipher import AES , PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from io import BytesIO

import base64
import zlib

KEY_NAME = "key"

def generate()->None:
    '''generate RSA key and store them in local file'''
    new_key = RSA.generate(2048)
    private_key = new_key.exportKey()
    public_key = new_key.publickey().exportKey()
    try:
        with open(f"{KEY_NAME}.pri","wb") as f:
            f.write(private_key)
        with open(f"{KEY_NAME}.pub","wb") as f:
            f.write(public_key)
    except IOError as err:
        print("Key generating failed!")
        print(err)

def get_rsa_cipher(key_type:str)->tuple:
    '''read file then return cipher object and the length of the key'''
    with open(f"{KEY_NAME}.{key_type}") as f:
        key = f.read()
    rsa_key = RSA.importKey(key)
    return (PKCS1_OAEP.new(rsa_key),rsa_key.size_in_bytes())

def encrypt(plain_text:bytes)->bytes:
    '''
    compress plain text -> generate session as AES key -> encrypt with AES key
    -> attach key and encrypted text -> encrypt with RSA private key 
    -> base64 encode
    '''
    compressed_text = zlib.compress(plain_text)
    session_key = get_random_bytes(16)
    cipher_aes = AES.new(session_key,AES.MODE_EAX)
    cipher_text , tag = cipher_aes.encrypt_and_digest(compressed_text)
    cipher_rsa , _ = get_rsa_cipher("pub")
    encrypted_session_key = cipher_rsa.encrypt(session_key)
    msg_payload = encrypted_session_key + cipher_aes.nonce + tag + cipher_text
    encrypted = base64.encodebytes(msg_payload)
    return encrypted

def decrypt(encrypted:bytes)->bytes:
    '''
    do anti-encrypt jobs
    base64 decode -> RSA decrypt with private key -> read AES session key
    -> AES decrypt -> decompress 
    '''
    encrypted_bytes = BytesIO(base64.decodebytes(encrypted))
    cipher_rsa , keysize_in_bytes = get_rsa_cipher("pri")
    encrypted_session_key = encrypted_bytes.read(keysize_in_bytes)
    nonce = encrypted_bytes.read(16)
    tag = encrypted_bytes.read(16)
    cipher_text = encrypted_bytes.read()

    session_key = cipher_rsa.decrypt(encrypted_session_key)
    cipher_aes = AES.new(session_key,AES.MODE_EAX,nonce)
    decrpyted = cipher_aes.decrypt_and_verify(cipher_text,tag)
    plain_text = zlib.decompress(decrpyted)
    return plain_text

if __name__ == "__main__":
    generate()
    plain_text = b"HelloWorld!"
    print(decrypt(encrypt(plain_text)))
