import socket as S
import threading as T

Clients = []
Client = {}

def handler(client_socket,client_address):
    print("Connected by",client_address)
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        else:
             data =  " " + str(Client[client_address[1]]) + " --> " + data.decode("utf-8")
             SendMsg(client_socket , data)
def SendMsg(clientS,msg):
    for client in Clients:
        if client != clientS:
            client.send(msg.encode("utf-8"))
            
host = '192.168.1.23'
port = 12345
Server = S.socket(S.AF_INET,S.SOCK_STREAM)
Server.bind((host,port))
Server.listen(3)

print("Server is Online:")
while True:
    client_S,client_A = Server.accept()
    data = client_S.recv(1024)
    data = data.decode("utf-8")
    Client.update({client_A[1] : data})    
    Clients.append(client_S)
    
    print(Client[client_A[1]])
    
    new_thread = T.Thread(target=handler,args=(client_S,client_A))
    new_thread.start()

#It will remain online as GroupChat is always available for clients to connect.