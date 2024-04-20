def xor_encrypt_decrypt(message, key):
    encrypted = ''.join(chr(ord(char) ^ key) for char in message)
    return encrypted
