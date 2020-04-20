# messaging server
# importing libraries
import socket
import sys
import threading
import json
import random
import time

class Server:
    MaxClient = 10   # total clients to be handled at a time
    # OnlineClients = {}  # available clients
    Groups = {}     # Groups members with there IDs
    # Groups = {GroupID:[Group Members List]}
    GroupNames = {}     # saves the name and Group id
    # GroupNames = {'groupID':'group Name'}
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

    def GetID(self, sock):
        print("finding id ...")
        for id, s in self.ClientsSockets.items():
            if s == sock:
                MyId = id
                print("id found ...")
        return id

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

    def CheckBuffer(self, stime):
        while True:
            time.sleep(stime)
            print("checking bufffer ...")
            pass


    def SendMessage(self, msg, id, sock):
        # first checking id
        print("message sending request ...")
        if id[0] == 'g':    # its a grou;s id
            print("a group id ...")
            for i, s in self.ClientsSockets.items():
                if s == sock:
                    MyId = i
            for EachMember in self.Groups[id]:
                print("sending message to client :", EachMember)
                if EachMember in self.ClientsSockets.keys():
                    print("client is online ...")
                    print("sending message ...")
                    temp = "In Group:"+self.GroupNames[id]+" By"
                    temp = temp + "<" + str(MyId) + "<" + msg
                    self.ClientsSockets[EachMember].sendall(temp.encode('UTF-8'))
                    print("message sent ...")

                else:
                    print("client is not online ...")
                    print("adding message to buffer for sending latter ...")
                    self.Buffer[str(EachMember)] = []
                    self.Buffer[str(EachMember)].append(msg)
                    print("added to buffer ...")
                    print(self.Buffer)
        else:
            for i, s in self.ClientsSockets.items():
                if s == sock:
                    MyId = i
            print("a client's id ...")
            if id in self.ClientsSockets.keys():
                print("client is online ...")
                print("sending message ...")
                temp = MyId + "<" + msg
                self.ClientsSockets[id].sendall(temp.encode('UTF-8'))
                print("sent ...")
            else:
                print("client is not online ...")
                print("adding to buffer ...")
                self.Buffer[str(id)] = []
                self.Buffer[id].append(msg)
                print("added ...")

    def Info(self, msg, sock):
        print(msg)
        print("got an info request ...")
        rep = ''
        print("gathering info ...")
        # if requests is for Group ID than
        # r<info<gID
        # len(msg) == 1 beacuse only one group ID will be passed
        # and only one client ID can also be passed as well
        # so checking weather a group ID of not will be like
        # msg[0][0] == 'g' mean a group ID
        # other wise it will be Clients ID
        if msg[0][0] == 'g': # group members request
            for EachId in self.Groups[msg[0]]:  # getting info of group members
                print("for EachId in msg:", EachId)
                if EachId in self.CurrentClientStatus.keys():
                    print("if EachId in self.CurrentClientStatus.keys():", EachId)
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
        else:
            for EachId in msg:
                print("for EachId in msg:", EachId)
                if EachId in self.CurrentClientStatus.keys():
                    print("if EachId in self.CurrentClientStatus.keys():", EachId)
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

    def CreateGroup(self, msg, sock):
        print("request for create a new group ...")
        print("Generating Random key ...")
        temp = random.randint(0, 10000)
        temp = str(temp)
        temp = "g" + temp
        # msg = ['Group Name','group members']
        if temp not in self.Groups.keys():
            print("Adding to Group to list ...")
            self.Groups[temp] = []
            print("updating GroupNames ...")
            self.GroupNames[temp] = str(msg[0])
            print("updated ...")
            print(self.GroupNames)
            for EachId in str(msg[1]).split(":")[:-2]:
                print("adding members to groups ...")
                self.Groups[temp].append(str(EachId))
            for id, s in self.ClientsSockets.items():   # finding id of the requester
                if s == sock:
                    print("adding members to groups ...")
                    self.Groups[temp].append(str(id))
            print("Added Successfully ...")
            print(self.Groups)
            print("Adding Group Admin ...")
            for id, s in self.ClientsSockets.items():
                if s == sock:
                    self.Admins[str(temp)] = str(id)
            print(self.Admins)
            print("updated ...")
            print("Sending key to Client ...")
            sock.sendall(temp.encode('UTF-8'))
            print("Sended Successfully ...")
        else:
            print("Key is present already ...")
            self.CreateGroup(msg, sock)

    def ChangeAdmin(self, msg, sock):
        # formate
        # c<ca<Group_ID<New_Admin_ID
        # here msg = ['Group_ID','New_Admin_ID']
        print("request for changing admin ...")
        if sock in self.ClientsSockets.values():
            print("socket found ...")
            print("finding id of requester ...")
            MyId = self.GetID(sock)
            print("Conferming admin ...")
            if self.Admins[msg[1]] == MyId:  # admin id matched
                print("confermed admin ...")
                print("changing admin ...")
                self.Admins[msg[1]] = msg[0] # setting new Admin
                print("admin changed ...")
                print(self.Admins)
                rep = "Admin changed to " + msg[0]
                print("sending reply to client ...")
                sock.sendall(rep.encode('UTF-8'))
                print("sent ...")
            else:
                rep = "You are not the admin of this group"
                print("sending reply to client ...")
                sock.sendall(rep.encode('UTF-8'))
                print("sent ...")

    def RemoveFromGroup(self,  msg, sock):
        pass

    def AddToGroup(self,  msg, sock):
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
        if msg[0] == 'c':
            if msg[1] == 'cg':   # create group
                self.CreateGroup(msg[2:], sock)
            if msg[1] == 'rfg':  # remove from group
                self.RemoveFromGroup(msg[2:], sock)
            if msg[1] == 'atg':     # add to group
                self.AddToGroup(msg[2:], sock)
            if msg[1] == 'ca': # change admin
                self.ChangeAdmin(msg[2:], sock)
        if msg[0] == 'm':
            self.SendMessage(msg[2], msg[1], sock)


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
            sys.exit(err)
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