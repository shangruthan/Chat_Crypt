import socket
import threading

def handle_client(client_socket, client_id, clients, encryption_key):
    while True:
        try:
            encrypted_message = client_socket.recv(1024).decode("utf-8")
            if not encrypted_message:
                break
            print(f"Encrypted message received from Client {client_id}: {encrypted_message}")
            
            for other_client_socket in clients:
                if other_client_socket and other_client_socket != client_socket:
                    other_client_socket.send(encrypted_message.encode('utf-8'))
                    print(f"Encrypted message sent from Client {client_id} to another client")
        except Exception as e:
            print(f"Error handling client {client_id}: {e}")
            break
    client_exit(client_id, clients)

def client_exit(client_id, clients):
    if clients[client_id]:
        clients[client_id].close()
    clients[client_id] = None

host = '127.0.0.1'
port = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(2)

clients = [None, None]

print("Waiting for clients to connect...")
for i in range(2):
    client_socket, addr = server.accept()
    print(f"Connected to {addr}")
    clients[i] = client_socket
    client_thread = threading.Thread(target=handle_client, args=(client_socket, i, clients, None))
    client_thread.start()

while not all(client is None for client in clients):
    pass

server.close()
