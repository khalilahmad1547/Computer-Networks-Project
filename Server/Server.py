# messaging server
# importing libraries
import socket
import sys
import threading
import json
import random

class Server:
    MaxClient = 5   # total clients to be handled at a time
    # OnlineClients = {}  # available clients
    Groups = {}     # Groups Name with there IDs
    # Groups = {GroupID:[Group Members List]}
    Admins = {}     # Each Group's Admin ID and Group's ID
    # Admins = {GroupID:Group_Admin_ID}
    ClientsSockets = {}    # Each Clients ID and Socket(if available)
    # Clients = {Clients_ID:Client_Socket}
    CurrentClientStatus = {}    # Each Client's ID with its Sign In status
    # CurrentClientStatus = {ClientID:'True/False'}
    ClientPass = {}     # Each Client's ID with its Password
    # ClientPass = {Client_ID:Password}
    Buffer = {}     # to store un sended data with id
    # Buffer = {ID:Message}

    def SignIn(self, id, password, sock):
        print("Sign in request form ", sock)
        if str(id) in str(self.ClientPass.keys()):
            print("ID found ...")
            if str(self.ClientPass[id]) == str(password):
                print("Password matched ...")
                rep = 'True'
                sock.sendall(rep.encode('UTF-8'))
                print(self.ClientPass)
                print("Adding Client's Socket to Available Clients Lists ...")
                self.ClientsSockets[str(id)] = sock
                print("added successfully ...")
                print("available clients are ")
                print(self.ClientsSockets)
                print("updating Client's status ...")
                self.CurrentClientStatus[str(id)] = 'online'
                print("updated successfully ...")
                print(self.CurrentClientStatus)
            else:
                print("Password not matched ...")
                rep = 'False'
                sock.sendall(rep.encode('UTF-8'))
        else:
            print("ID not present ...")
            rep = 'False'
            sock.sendall(rep.encode('UTF-8'))

    def SignUp(self, password, sock):
        # print("New Sign Up request ...")
        print("Generating Random key ...")
        temp = random.randint(0, 10000)
        temp = str(temp)
        if temp not in self.ClientPass.keys():
            print("Adding to Client's list ...")
            self.ClientPass[temp] = str(password)
            print(self.ClientPass)
            print("Added Successfully ...")
            print("Sending key to Client ...")
            sock.sendall(temp.encode('UTF-8'))
            print("Sended Successfully ...")
            print("updating Client's status ...")
            self.CurrentClientStatus[str(temp)] = 'offline'
            print("updated successfully ...")
            print(self.CurrentClientStatus)
        else:
            print("Key is present already ...")
            self.SignUp(password)

    def Info(self, msg, sock):
        print(msg)
        print("got an info request ...")
        rep = ''
        print("gathering info ...")
        for EachId in msg:
            print("for EachId in msg:",EachId)
            if EachId in self.CurrentClientStatus.keys():
                print("if EachId in self.CurrentClientStatus.keys():",EachId)
                if self.CurrentClientStatus[EachId] == 'online':
                    print("if self.CurrentClientStatus[EachId]:", EachId)
                    rep = rep + str(EachId) + ":online<"
                    print(rep)
                else:
                    print("else:")
                    rep = rep + str(EachId) + ":offline<"
                    print(rep)
            else:
                rep = rep + str(EachId) + ":Not found<"
        print("gathered ...")
        print(rep)
        print("sending to client ...")
        sock.sendall(str(rep).encode('UTF-8'))
        print("sent ...")

    def CreateGroup(self):
        pass

    def Decoder(self, msg, sock):
        msg = msg.split("<")
        print(msg)
        if msg[0] == 'r':
            if msg[1] == 'in':
                try:
                    self.SignIn(msg[2], msg[3], sock)
                except IndexError as err:
                    print("Error in msg ...")
                    print(err)
                    rep = 'False'
                    sock.sendall(rep.encode('UTF-8'))
                else:
                    pass
            if msg[1] == 'up':
                try:
                    self.SignUp(msg[2], sock)
                except IndexError as err:
                    print("ERROR in message ...")
            if msg[1] == 'info':
                try:
                    self.Info(msg[2:], sock)
                except IndexError as err:
                    print("error in index ", err)


    def Handler(self, sock, adr):
        while True:
            msg = sock.recv(1024)
            msg = msg.decode('UTF-8')
            if not msg:
                if sock in self.ClientsSockets.values():
                    for id, s in self.ClientsSockets.items():
                        if sock == s:
                            print("deleting Socket from list ...")
                            del self.ClientsSockets[id]
                            print("deleted ...")
                            print(self.ClientsSockets)
                            print("updating client's status ...")
                            self.CurrentClientStatus[id] = 'offline'
                            print("updated ...")
                            print(self.CurrentClientStatus)
                            break
                break
            else:
                self.Decoder(msg, sock)



    def __init__(self):
        try:
            print("Creating Socket ...")
            self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print("Socket creating error :", err)
            sys.exit("Socket creating error ")
        ServerIP = 'localhost'
        ServerPort = 8080
        ServerAdress = (ServerIP, ServerPort)
        try:
            print("Running Server at address :", ServerAdress)
            self.Socket.bind(ServerAdress)
        except socket.error as err:
            print("Socket Binding error :", err)
        else:
            print("Server Running Successfully")

        self.Socket.listen(self.MaxClient)
        while True:
            print("Waiting for connections")
            ClientSocket, ClientAdress = self.Socket.accept()
            print("got a connection from ", ClientAdress)
            newClient = threading.Thread(target=self.Handler, args=(ClientSocket, ClientAdress))
            newClient.start()


if __name__ == '__main__':
    MyServer = Server()