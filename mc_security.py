#############################################################
# mc_security.py                                            #
#                                                           #
# by: K.Imber                                               #
#                                                           #
# set of functions for hashing and testing authentication   #
#############################################################

import hashlib
import getpass

SEPARATOR = ":::"
FILENAME = "pass.txt"

def get_creds(setting=False):
    user_name = raw_input("Username: ")
    if setting:
        while True:
            user_pass = getpass.getpass()
            print "Please re-enter your password to confirm"
            repeated = getpass.getpass()
            if repeated != user_pass:
                print "Passwords don't match.  Please try again."
                print "*****************************************"
            else:
                break
    else:
        user_pass = getpass.getpass()
    return user_name, user_pass

def add_new_user_to_pass_store():
    uname, upass = get_creds(True)
    line = build_user_line(uname, upass)
    pass_file = open(FILENAME, "a")
    pass_file.write(line + "\n")
    pass_file.close()

def hash_user(uname, upass):
    hasher = hashlib.sha512()
    hasher.update(uname)
    hasher.update(upass)
    return hasher.hexdigest()

def build_user_line(uname, upass):
    user_hash = hash_user(uname, upass)
    return uname + SEPARATOR + user_hash

def get_user(client_data_line):
    return client_data_line.split(SEPARATOR)[0]

def try_authentication(client_data_line):
    uname = client_data_line.split(SEPARATOR)[0]
    client_hash = client_data_line.split(SEPARATOR)[1]
    
    pass_file = open(FILENAME, "r")
    lines = pass_file.readlines()
    pass_file.close()

    for i in range(len(lines)):
        if lines[i].startswith(uname):
            recorded_hash = lines[i].split(SEPARATOR)[1].strip()
##            print "Comparing \nclient_hash (in from the client): '" + client_hash + "'"
##            print "recorded_hash (from the pass file): '" + recorded_hash + "'"
##            print "Returning " + str(recorded_hash == client_hash) + "."
            return recorded_hash == client_hash


if __name__ == '__main__':
    print "Please create credentials for new user"
    add_new_user_to_pass_store()
    print "User added to pass file. Exiting."
