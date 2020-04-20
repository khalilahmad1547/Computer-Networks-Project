# messaging lient
# importing libraries
import socket
import sys
import json

class Client:
    MyName = None     # My user name
    MyId = None   # My unique Id stored in server
    MyGroups = {}   # Groups which I have joined
    # MyGroups = {'Group Id':'Group Name'}
    MyContacts = {}     # List of contacts which i have saved
    # MyContacts = {'ID':'Name'}
    MyStatus = False   # I am online or offline
    Socket = None     # socket

    def SendMessage(self,):
        pass

    def RecvMessage(self):
        pass

    def EncodeMessage(self, msg):
        pass

    def SaveData(self):
        if self.MyStatus is True:
            with open("MyContacts.json", 'w') as File:
                json.dump(self.MyContacts, File)
            with open("MyGroups.json", 'w') as File:
                json.dump(self.MyGroups, File)
        else:
            print("Please Sign in")

    def LoadData(self):
        if self.MyStatus is True:
            try:
                File = open("MyContacts.json")
                self.MyContacts = json.load(File)
            except FileNotFoundError as err:
                print("No Saved Data found")
            else:
                print("Data Loaded successfully")
            try:
                File = open("MyGroups.json")
                self.MyGroups = json.load(File)
            except FileNotFoundError as err:
                print("No Saved Data found")
            else:
                print("Data Loaded successfully")

        else:
            print("Please Sign in")

    def Contacts(self):
        if self.MyStatus is True:
            msg = "r<info"
            # "r<info<id<id" format
            if len(self.MyContacts) == 0:   # empty no saved contacts
                print("NO Saved Contacts")
            else:   # no empty conatacts are saved
                for id, name in self.MyContacts.items():
                    msg = msg + "<" + str(id)
                self.Socket.sendall(msg.encode('UTF-8'))
                info = self.Socket.recv(1024).decode('UTF-8')
                info = info.split("<")
                for EachInfo in info[:-1]:
                    EachInfo = EachInfo.split(":")
                    if EachInfo[0] in self.MyContacts.keys():
                        print(f"Name :{self.MyContacts[EachInfo[0]]}", f"ID :{EachInfo[0]}", f"status :{EachInfo[1]}",
                              sep='     ')
                    else:
                        print(f"Name :Not Saved", f"ID :{EachInfo[0]}", f"status :{EachInfo[1]}", sep='     ')

        else:
            print("Please Sign in")

    def GroupMembers(self):
        if self.MyStatus is True:
            msg = "r<info<"
            # "r<info<'group ID'" format
            # printing joined groups
            for gID, Name in self.MyGroups.items():
                print(f"Group ID :{gID} Group Name :{Name}")
            gID = input("Enter Group ID :")
            msg = msg + gID
            self.Socket.sendall(msg.encode('UTF-8'))
            info = self.Socket.recv(1024).decode('UTF-8')
            info = info.split("<")
            for EachInfo in info[:-1]:
                EachInfo = EachInfo.split(":")
                if EachInfo[0] in self.MyContacts.keys():
                    print(f"Name :{self.MyContacts[EachInfo[0]]}", f"ID :{EachInfo[0]}", f"status :{EachInfo[1]}", sep='     ')
                elif EachInfo[0] == self.MyId:
                    print(f"You ", f"ID :{EachInfo[0]}", f"status :{EachInfo[1]}", sep='     ')
                else:
                    print(f"Name :Not Saved", f"ID :{EachInfo[0]}", f"status :{EachInfo[1]}", sep='     ')
        else:
            print("Please Sign in")

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

    def CreateGroup(self):
        tname = input("Enter Group Name :")
        rep = "c<cg<"+tname + "<"
        a = None
        print("Enter 'end' to exit")
        while a != 'end':
            a = input("Enter User Id to Add in this Group:")
            rep = rep + a + ":"
        self.Socket.sendall(rep.encode('UTF-8'))
        a = self.Socket.recv(1024)
        a = a.decode('UTF-8')
        self.MyGroups[str(a)] = tname
        print(self.MyGroups)

    def ChangeAdmin(self):
        # formate
        # c<ca<Group_ID<New_Admin_ID
        command = "c<ca<"
        print("Your Groups :")
        print(self.MyGroups)
        gid = input("Enter group Id :")
        self.Contacts()
        id = input("Enter New Admins ID :")
        command = command + str(id)+ "<" + str(gid)
        self.Socket.sendall(command.encode('UTF-8'))
        rep = self.Socket.recv(1024)
        print(rep.decode('UTF-8'))

    def RemoveFromGroup(self):
        pass

    def AddToGroup(self):
        pass

    def GoOffline(self):    # will disconnect from server
        self.Socket.close()
        self.Socket = None
        self.MyStatus = False

    def AddContact(self):   # will add new contact
        if self.MyStatus is True:
            tid = input("Enter ID :")
            tname = input("Enter Name :")
            if tid not in self.MyContacts.keys():
                self.MyContacts[str(tid)] = tname
                print("Added successfully")
            else:
                print("User Already Exist")
        else:
            print("Please Sign in")

    def MyProfile(self):    # will print My basics info
        if self.MyStatus is True:
            print("User Name :", self.MyName)
            print("User ID :", self.MyId)

    def Chat(self):
        print("1. In group")
        print("2. with client")
        print("3. Exist")
        t = input(">>>")
        if t == '1':
            print(self.MyGroups)
            OtherClient = input("Enter Group ID :")
            msg = input(">>>")
            while msg!='\end':
                if msg == '.':
                    pass
                else:
                    msg = "m<" + OtherClient + "<" + msg
                    self.Socket.sendall(msg.encode('UTF-8'))
                try:
                    print(self.Socket.recv(1024).decode('UTF-8'))
                    msg = input(">>>")
                except KeyboardInterrupt:
                    pass
        if t == '2':
            print(self.MyContacts)
            OtherClient = input("Enter Client's ID :")
            msg = input(">>>")
            while msg != '\end':
                if msg == '.':
                    print(self.Socket.recv(1024).decode('UTF-8'))
                    msg = input(">>>")
                else:
                    msg = "m<" + OtherClient + "<" + msg
                    self.Socket.sendall(msg.encode('UTF-8'))
                    print(self.Socket.recv(1024).decode('UTF-8'))
                    msg = input(">>>")


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
                    #print("loading data")
                    #self.LoadData()
            else:
                print("1. Create New Group")
                print("2. Change Group Admin")
                print("3. Add to Group")
                print("4. Remove from Group")
                print("5. Chat")
                print("6. Go Offline")
                print("7. My Profile")
                print("8. Add New Contact")
                print("9. Contacts")
                print("a. View Group Members")
                print("b. Exit")
                temp = input(">>>")
                if temp is '1':
                    self.CreateGroup()
                elif temp is '2':
                    self.ChangeAdmin()
                elif temp is '3':
                    self.AddToGroup()
                elif temp is '4':
                    self.RemoveFromGroup()
                elif temp is '5':
                    self.Chat()
                elif temp is '6':
                    self.GoOffline()
                elif temp is '7':
                    self.MyProfile()
                elif temp is '8':
                    self.AddContact()
                elif temp is '9':
                    self.Contacts()
                elif temp is 'a':
                    self.GroupMembers()
                elif temp is 'b':
                    #self.SaveData()
                    self.Socket.close()
                    break
                else:
                    print("Please Enter a Valid Option")

    def __init__(self):
        try:
            self.Decoder()
        except KeyboardInterrupt:
            print("saving data ")
            #self.SaveData()
            print("Saved data")


if __name__ == '__main__':
    MyClient = Client()