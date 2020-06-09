# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 12:01:23 2020

@author: Abdullah
"""

import socket as S
import threading as T

def Receive(client):
    while True:
        msg = client.recv(1024)
        print(msg.decode("utf-8"))
        
client_socket = S.socket(S.AF_INET, S.SOCK_STREAM)
host = 'localhost'
port = 12345
client_socket.connect((host,port))
print("Connected\nWelcome to chatRoom:")
thread =T.Thread(target=Receive , args=(client_socket,))
thread.start()

msg = input("Enter name: ")
client_socket.send(msg.encode("utf-8"))
    
while True:
    
    msg = input("You:")

    client_socket.send(msg.encode("utf-8"))
    
client_socket.close()