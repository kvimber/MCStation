import socket
import properties
import getpass
import hashlib
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
        user_name = raw_input("Username: ")
        user_pass = getpass.getpass()
        to_send = mc_sec.build_user_line(user_name, user_pass)
        print "sending '" + to_send + "'"
        self.s.send(to_send)
        data = self.s.recv(1024)
        if data == 'Authenticated':
            print "Authentication succeeded as user " + user_name + "."
        else :
            print "Authentication failed. Please try again."
            self.authenticate()
        

    def run_cli(self):
        while True:
            inp = raw_input("#> ")
            if inp == "quit":
                print "Quitting..."
                break
            elif inp == "help":
                self.print_help()
            elif inp.startswith("/"):
                self.s.send(inp)
            else:
                if self.validate(inp):
                    self.s.send(inp)
                else:
                    print "Command failed validation.  Type help for more information."
            data = self.s.recv(1024)
            print "Received reply from server: '" + data + "'"
        self.close()

    def print_help(self):
        print "Help System Printing Now."
        print "Oops, this is just a stub.  Looks like you're on your own for now"
        print "End."


    def close(self):
        self.s.close()
        print "Socket closed. Exiting."

    def validate(self, cmd):
        return True

if __name__ == '__main__':
    c = MCClient()
    c.run_cli()
