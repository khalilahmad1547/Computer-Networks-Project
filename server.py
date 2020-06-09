# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 11:50:10 2020

@author: Abdullah
"""

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
            
host = 'localhost'
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