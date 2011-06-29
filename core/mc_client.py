import socket
import properties
import mc_security as mc_sec

class MCClient:

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = properties.PROPS[properties.SERVER_HOST]
        port = properties.PROPS[properties.SERVER_PORT]
        self.s.connect((host, port))
        print "Connected to " + host + " at port " + str(port) + "."
        self.authenticate()

    def authenticate(self):
        uname, upass = mc_sec.get_creds()
        to_send = mc_sec.build_user_line(uname, upass)
##        print "sending '" + to_send + "'"
        print "Sending authentication..."
        self.s.send(to_send)
        data = self.s.recv(1024)
        if data == 'Authenticated':
            print "Authentication succeeded as user " + uname + "."
        else :
            print "Authentication failed. Please try again."
            self.authenticate()
        

    def run_cli(self):
        while True:
            inp = raw_input("#> ")
            if inp == "quit":
                print "Quitting..."
                break
            else:
                self.s.send(inp)
            data = []
            recvd = self.s.recv(1024).split("\n")
##            print "Received from server: "
##            print recvd
            for i in range(len(recvd)):
                data.append(recvd[i])
            while not data[len(data)-1].startswith("MCServer command received correctly."):
                recvd = self.s.recv(1024).split("\n")
##                print "Received from server: "
##                print recvd
                for i in range(len(recvd)):
                    data.append(recvd[i])
##            print "Received reply from server:"
##            print data
            for i in range(len(data)-1):
                print data[i]
        self.close()

    def close(self):
        self.s.close()
        print "Socket closed. Exiting."

if __name__ == '__main__':
    c = MCClient()
    c.run_cli()
