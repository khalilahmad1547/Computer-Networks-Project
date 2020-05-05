import socket as S
import threading as T

def Receive(client):
    while True:
        msg = client.recv(1024)
        print(msg.decode("utf-8"))
client_socket = S.socket(S.AF_INET, S.SOCK_STREAM)
host = '192.168.1.23'
port = 12345
client_socket.connect((host,port))
print("Connected\nWelcome to chatRoom:")
thread =T.Thread(target=Receive , args=(client_socket,))
thread.start()

while True:
    a = input("Enter option \n 1. Send message in group \n 2. Send message to other client")
    msg = input("You:")
    msg = a + msg
    client_socket.send(msg.encode("utf-8"))
    
client_socket.close()