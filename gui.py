import socket
from threading import Thread
from encryption import xor_encrypt_decrypt
import PySimpleGUI as sg

# Function to send messages
def send_message():
    message = values['_INPUT_']
    encrypted_message = xor_encrypt_decrypt(message, 10)
    client_socket.send(encrypted_message.encode('utf-8'))
    window['_CHAT_HISTORY_'].print("You: " + message, text_color='blue')
    window['_INPUT_']('')
    
# Function to receive messages
def receive_message():
    while True:
        try:
            received_message = client_socket.recv(1024).decode('utf-8')
            decrypted_message = xor_encrypt_decrypt(received_message, 10)
            window['_CHAT_HISTORY_'].print("Buddy: " + decrypted_message + '\n', text_color='green')
        except ConnectionResetError:
            break

# Function to establish a connection to the server
def connect_to_server():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 9090))
    receive_thread = Thread(target=receive_message)
    receive_thread.daemon = True
    receive_thread.start()

#  the layout
layout = [
    [sg.Text('Dialogue Box', font=('Helvetica', 11, 'bold'), justification='center', text_color='black')],
    [sg.Output(size=(60, 20), key='_CHAT_HISTORY_', background_color='lightgrey', text_color='black')],
    [sg.Text('Drop a Line Here', font=('Helvetica', 9), text_color='black'), 
     sg.InputText(key='_INPUT_', size=(35, 1), text_color='black', background_color='lightblue'),
     sg.Button('▶', button_color=('white', 'green'), key='_SEND_', size=(2, 1))]
]

# Create the window
window = sg.Window('CHAT CRYPT', layout, element_justification='c', background_color='lightgrey')

# Establish the connection to the server
connect_to_server()

# Event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == '_SEND_':
        send_message()

window.close()