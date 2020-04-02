# messaging lient
# importing libraries
import socket
import sys


class Client:
    MyName = ''
    Socket = ''
    OtherClient = ''
    OnlineClients = ''

    def SendMessage(self,):
        print(self.OnlineClients)
        self.OtherClient = input("Enter user to connect :")
        msg = input(">>> ")
        msg = self.EncodeMessage(msg)
        Client.Socket.sendall(msg)
        return msg.decode('UTF-8')

    def RecvMessage(self):
        msg = self.Socket.recv(1024)
        print(msg.decode('UTF-8'))

    def EncodeMessage(self, msg):
        msg = self.OtherClient + "<" + msg
        msg = msg.encode('UTF-8')
        return msg

    def regester(self):
        Client.Socket.sendall(Client.MyName.encode('UTF-8'))
        Client.OnlineClients = Client.Socket.recv(1024)
        Client.OnlineClients = Client.OnlineClients.decode('UTF-8')


    def close(self):
        try:
            print("closing socket")
            Client.Socket.close()
        except socket.error as err:
            print("socket closing error :",err)
            sys.exit("Socket closing error")


    def __init__(self):
        try:
            Client.MyName = input("Enter user name :")
            print("Creating Socket")
            Client.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print("Socket creating error :", err)
            sys.exit("Socket creating error ")

        ServerIP = 'localhost'
        ServerPort = 8080
        ServerAdress = (ServerIP, ServerPort)


        try:
            print("connecting to server :", ServerAdress)
            Client.Socket.connect(ServerAdress)
        except socket.error as err:
            print("error in connecting to server :", err)
            sys.exit("error in connecting to server :")
        else:
            print("connected to the server")
        self.regester()
        '''msg = ''
                while msg != '\end':
                    msg = self.SendMessage(self.Socket)
                self.Socket.close()'''


if __name__ == '__main__':
    MyClient = Client()
    msg = ''
    while msg!='\end':
        msg = MyClient.SendMessage()
        MyClient.RecvMessage()
    MyClient.close()