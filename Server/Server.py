# messaging server
# importing libraries
import socket
import sys
import threading


class Server:
    # total clients to be handled at a time
    MaxClient = 5
    # available clients
    OnlineClients = {}

    def DecodeMessage(self, msg):
        msg = msg.decode('UTF-8')
        msg = msg.split("<")
        return msg

    def Handler(self, sock, adr):
        # print("Got A connection from :",adr)
        # self.ClientName = ''
        # self.ClientName = "Please tell us you name :"
        ClientName = sock.recv(1024)
        ClientName = ClientName.decode('UTF-8')
        print(ClientName)
        Server.OnlineClients[ClientName] = sock
        print("client ",ClientName," added to lsit")
        print(self.OnlineClients)
        sock.sendall(str(Server.OnlineClients.keys()).encode('UTF-8'))
        while True:
            msg = self.DecodeMessage(sock.recv(1024))
            print(msg)
            Server.OnlineClients[str(msg[0])].sendall(str(msg[1]).encode('UTF-8'))
            if not msg[1]:
                del Server.OnlineClients[ClientName]
                print(Server.OnlineClients)
                break
            else:
                print("Message from :", adr, msg[1], " to ", Server.OnlineClients[str(msg[0])])


    def __init__(self):
        try:
            print("Creating Socket")
            Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print("Socket creating error :", err)
            sys.exit("Socket creating error ")
        ServerIP = 'localhost'
        ServerPort = 8080
        ServerAdress = (ServerIP, ServerPort)
        try:
            print("Running Server at address :", ServerAdress)
            Socket.bind(ServerAdress)
        except socket.error as err:
            print("Socket Binding error :", err)
        else:
            print("Server Running Successfully")

        Socket.listen(Server.MaxClient)
        while True:
            print("Waiting for connections")
            ClientSocket, ClientAdress = Socket.accept()
            print("got a connection from ", ClientAdress)
            newClient = threading.Thread(target=self.Handler, args=(ClientSocket, ClientAdress))
            newClient.start()


if __name__ == '__main__':
    MyServer = Server()