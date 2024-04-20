import socket
from encryption import xor_encrypt_decrypt

host = '127.0.0.1'
port = 9090

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

while True:
    message = input("Enter a message to send to the server: ")
    encrypted_message = xor_encrypt_decrypt(message, 10)  # Encrypt the message
    client.send(encrypted_message.encode('utf-8'))

    received_message = client.recv(1024).decode('utf-8')
    decrypted_message = xor_encrypt_decrypt(received_message, 10)  # Decrypt the received message
    print(f"Decrypted message received from the server: {decrypted_message}")

client.close()
