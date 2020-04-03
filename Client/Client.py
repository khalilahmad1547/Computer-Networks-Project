# messaging lient
# importing libraries
import socket
import sys
import json

class Client:
    MyName = None     # My user name
    MyId = None   # My unique Id stored in server
    MyGroups = {}   # Groups which I have joined
    # MyGroups = {'Group Name':group_Id}
    MyContacts = {}     # List of contacts which i have saved
    # MyContacts = {Contact_Name:His_ID}
    MyStatus = False   # I am online or offline
    Socket = None     # socket
    OtherClient = None        # to which client of group i am chatting
    OnlineClients = None      # other online clients

    def SendMessage(self,):
        print(self.OnlineClients)
        self.OtherClient = input("Enter user to connect :")
        msg = input(">>> ")
        msg = self.EncodeMessage(msg)
        self.Socket.sendall(msg)
        return msg.decode('UTF-8')

    def RecvMessage(self):
        msg = self.Socket.recv(1024)
        print(msg.decode('UTF-8'))

    def EncodeMessage(self, msg):
        msg = self.OtherClient + "<" + msg
        msg = msg.encode('UTF-8')
        return msg

    def SignUp(self):   # will do sign Up
        self.MyName = input("Enter your User Name :")
        temp = input("Enter Your Password :")
        temp = "r<up<"+ temp
        self.Socket.sendall(temp.encode('UTF-8'))
        self.MyId = self.Socket.recv(1024).decode('UTF-8')
        print("Sign Up Successfully")
        print("Your user name :", self.MyName)
        print("Your ID is :", self.MyId)

    def SignIn(self):   # will do sign in
        if self.MyName is None:
            self.MyName = input("Enter User Name :")
        if self.MyId is None:
            self.MyId = input("Enter Your ID :")
        temp = input("Enter Your Password :")
        temp = "r<in<"+str(self.MyId)+"<"+str(temp)
        self.Socket.sendall(temp.encode('UTF-8'))
        temp = self.Socket.recv(1024)
        if temp.decode('UTF-8') == 'True':
            print("Sign in successful")
            self.MyStatus = True
        else:
            print("Try again")
            self.SignIn()

    def CreateGroup(self):  # will create a New group
        pass

    def GoOffline(self):    # will disconnect from server
        pass

    def AddContact(self):   # will add new contact
        pass

    def MyProfile(self):    # will print My basics info
        pass

    def Chat(self):
        pass

    def close(self):
        try:
            print("closing socket")
            self.Socket.close()
        except socket.error as err:
            print("socket closing error :",err)
            sys.exit("Socket closing error")

    def ConnectToServer(self):
        try:
            # self.MyName = input("Enter user name :")
            print("Creating Socket")
            self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print("Socket creating error :", err)
            sys.exit("Socket creating error ")
        ServerIP = 'localhost'
        ServerPort = 8080
        ServerAdress = (ServerIP, ServerPort)
        try:
            print("connecting to server :", ServerAdress)
            self.Socket.connect(ServerAdress)
        except socket.error as err:
            print("error in connecting to server :", err)
            sys.exit("error in connecting to server :")
        else:
            print("connected to the server")

    def Decoder(self):
        while True:
            if self.Socket is None:     # not connected to server
                print("1. Go Online")
                print("2. Exit")
                temp = input(">>>")
                if temp is '1':
                    self.ConnectToServer()
                elif temp is '2':
                    break
            elif self.MyStatus is False:     # I have't Sign in
                print("1. Sign UP")
                print("2. Sign In")
                temp = input(">>>")
                if temp is '1':
                    self.SignUp()
                elif temp is '2':
                    self.SignIn()
            else:
                print("1. Create New Group")
                print("2. Chat")
                print("3. Go Offline")
                print("4. Exit")
                temp = input(">>>")
                if temp is '1':
                    self.CreateGroup()
                elif temp is '2':
                    self.Chat()
                elif temp is '3':
                    self.GoOffline()
                elif temp is '4':
                    self.Socket.close()
                    break
                else:
                    print("Please Enter a Valid Option")

    def __init__(self):
        self.Decoder()


if __name__ == '__main__':
    MyClient = Client()