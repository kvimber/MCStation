#############################################################################
# mc_server.py                                                              #
#                                                                           #
# by: K.Imber                                                               #
# on: 5.23.11                                                               #
#                                                                           #
# runs the minecraft server and manages communication with it (hopefully)   #
#############################################################################

import shlex, subprocess        # for running cli commands
from datetime import datetime   # for parsing dates in logs
import mapper, mailer           # for running map generation and mailing
import socket                   # for networking the server
import threading                # for server threading
import properties               # for property handling
import time                     # for test setup method
import os
import mc_security as mc_sec

class MCServer:

    def __init__(self):
        print "MCStation initializing..."
        self.props = properties.PROPS
        self.p = None
        self.lock = threading.Lock()
        self.thread_id = 0
        self.check_platform()
        self.startup()
        print "MCStation initialized."

    #Validates the users system and properties
    def startup(self):
        self.check_java()
        self.check_minecraft()
        self.check_mapper()
        self.check_auth_system()
        # TODO: Check for mailer

    def check_auth_system(self):
        if not os.path.exists(mc_sec.FILENAME):
            print "No authentication available, please create a new user below:"
            mc_sec.add_new_user_to_pass_store()
        else:
            print "Authentication system ready."

    def check_mapper(self):
        # Checks to see if mapping utility can be found.
        try:
            self.props[properties.CLI_RUNMAPPER]
            if len(os.listdir(self.props[properties.PATH_MAPPER])) > 0:
                self.mapper_avail = True
            else:
                self.mapper_avail = False
        except KeyError:
            self.mapper_avail = False
##        self.mapper_avail = os.path.exists(self.props[properties.PATH_MAPPER])
##        print self.props[properties.PATH_MAPPER]
##        print os.path.exists(self.props[properties.PATH_MAPPER])
        if(self.mapper_avail):
            print "Mapping software found. Mapping functionality available for use"
        else:
            print "Mapping software not found. Add mapper to properties.py if you want to enable mapping functionality"


    def check_minecraft(self):
        # Checks to see if minecraft_server.jar can be found
        if(os.path.exists(self.props[properties.PATH_SERVER] + "/minecraft_server.jar")):
           print "Minecraft found"
        else:
           raise RuntimeError("Unable to find minecraft_server.jar. Double check PROPS[PATH_SERVER] in properties.py")

    def check_java(self):
        # Checks to see if java is available
        self.jtest = subprocess.Popen(shlex.split(self.java_cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (child_stdout, child_stderr) = self.jtest.communicate()
        if(child_stderr.startswith("java version")):
            print "Java found"
        else:
            raise RuntimeError("Unable to locate Java. Verify you have it installed and on your path")

    def start(self):
        if self.p is None:
            print "Setting up server instance..."
            cmd_list = shlex.split(self.props[properties.CLI_RUNSERVER])
            self.p = subprocess.Popen(cmd_list, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.watch_for_startup()
            print "Server up and running."

    def cmd(self, cmd):
        ''' Sends a command (cmd) to the running server instance'''
        if self.p is not None:
            self.p.stdin.write(cmd + "\n")

    def stop(self):
        if self.p is not None:
            print "System stopping..."
            self.cmd("stop")
            # for cleaning up, to worry about later: maybe a 'del' statement would be better?
            self.p = None
            print "System stopped."

    # log functions don't need a running system, they deal with the file system instead
    def get_logs(self):
        if os.path.exists(self.props[properties.PATH_LOGFILE]):
            f = open(self.props[properties.PATH_LOGFILE], "r")
            lines = f.readlines()
            f.close()
            return lines
        else:
            print "The server.log file hasn't been created yet, no logs to get."
            return []

    def get_logs_since(self, lastLoggedDate):
        ''' gets all logs newer than datetime object given (lastLoggedDate) '''
        logLines = self.get_logs()
        results = []
        for i in range(len(logLines)):
            if self.serverlog_to_datetime(logLines[i]) > lastLoggedDate:
                results.append(logLines[i])
        return results

    def format_logs(self, logs):
        ''' will print out a list of logs (logs) as outputted by the server '''
        for i in range(len(logs)):
            print logs[i],

    def get_logs_since_last_start(self):
        ''' returns all logs from last startup message '''
        logs = self.get_logs()
        results = []
        lastStart = 0
        for i in range(len(logs)):
            if logs[i].find(" Starting minecraft server version ") != -1:
                lastStart = i

        for i in range(lastStart, len(logs)):
            results.append(logs[i])
        return results
                    

    def serverlog_to_datetime(self, serverDateFormattedString):
        ''' converts server date format to a python datetime object '''
        ''' ie. '2011-05-24 17:39:50'.  Can take full log lines as well '''
        pieces = serverDateFormattedString.split(" ")
        curDate = pieces[0] + " " + pieces[1]
        return datetime.strptime(curDate, '%Y-%m-%d %H:%M:%S')

    # map and mailing functions
    def run_mapper(self):
        if(self.mapper_avail):
            mapTool = mapper.Mapper(self)
            mapTool.run()
        else:
            print "Mapping functionality not available. Please add a mapper in properties.py and restart server."

    def run_mapper_and_send(self, to_addr=None):
        if(self.mapper_avail):
            self.run_mapper()
            mailTool = mailer.Mailer(self)
            mailTool.sendMap(to_addr)
        else:
            print "Mapping functionality not available. Please add a mapper in properties.py and restart server."

    def run_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.props[properties.SERVER_HOST], self.props[properties.SERVER_PORT]))
        s.listen(5)
        print "Server waiting on connections, Ctrl+C to quit"
        while True:
            try:
                conn, addr = s.accept()
                print "Connect by", addr
                thread = ServerCmdThread(self, conn, self.thread_id)
                thread.start()
                self.thread_id += 1
                print "Thread " + thread.name + " started..."
            except KeyboardInterrupt:
                print "\nKeyboard Interrupt Occurred.  Exiting."
                self.stop()
                break

    def run_server_cmd(self, cmd):
        print "    Server command '" + str(cmd) + "' received.  Currently working on executing it."
        result = ""
        if cmd.startswith("/"):
            print "    Executing minecraft server command '" + cmd[1:] + "'."
            # currently doing NO OUTPUT?
            self.cmd(cmd[1:])
        else:
            result += self.run_mc_cmd(cmd)
        return result

    def run_mc_cmd(self, cmd):
        result = ""
        if cmd == "map":
            self.run_mapper()
            result += "Mapper Successfull Run.\n"
        elif cmd == "mapsend":
            self.run_mapper_and_send()
            result += "Map Successfully Created and Sent.\n"
        elif cmd == "getlogs":
            logs = self.get_logs_since_last_start()
            for i in range(len(logs)):
                result += logs[i]
        elif cmd == "start":
            self.start()
            result += "Minecraft Server Started.\n"
        elif cmd == "stop":
            self.stop()
            result += "Minecraft Server Stopped.\n"
        elif cmd == "help":
            result += self.build_help()
        else:
            result += "Could not parse command.  Type 'help' to get command list.\n"
        return result
                
            
    def build_help(self):
        result = ""
        result += "- Help - client commands listed below:\n"
        result += "start   - start the Minecraft server.\n"
        result += "stop    - stop the Minecraft server.\n"
        result += "getlogs - get the Minecraft server logs.\n"
        result += "map     - run the mapping system.\n"
        result += "mapsend - run the mapping system, and email it to yourself.\n"
        return result

    def run_test_setup(self):
        self.start()
        print "sleeping to let system start..."
        time.sleep(1)
        print "3"
        time.sleep(1)
        print "2"
        time.sleep(1)
        print "1"
        time.sleep(1)
        print "sleep finished. system startup logs below."
        print "*" * 30
        self.format_logs(self.get_logs_since_last_start())
        print "*" * 30
        print "running server now..."
        self.run_server()

    #Checks to see if running Unix or Windows. Any platform based modifications should be made here.
    def check_platform(self):
        self.java_cmd = "java -version"

    #Debug method used to print returns from the subprocess
    def debug(self):
        (stderr, stdout) = self.p.communicate()
        print "stdout"
        print stdout
        print "stderr"
        print stderr


    #Watches for '[INFO] Done' to be printed to log. If doesn't appear within a user defined number of seconds, throw an error
    def watch_for_startup(self):
        watch = True
        count = 0
        while(watch):
            try:
                time.sleep(1)
                logs = self.get_logs()
                print logs[-1], 
                if(logs[-1].find("[INFO] Done") != -1):
                    watch = False
                count += 1
                if(count>self.props[properties.CLI_TIMEOUT]):
                    watch = False
                    #self.debug()
                    raise RuntimeError("Error starting server")
            except IndexError:
                continue


class ServerCmdThread(threading.Thread):

    def __init__(self, serverInstance, conn, thread_id):
        threading.Thread.__init__(self, name="cmd" + str(thread_id))
        self.server = serverInstance
        self.conn = conn
        self.authenticated = False

    def run(self):
        while True:
            data = self.conn.recv(1024)
            if not self.authenticated:
                self.authenticated = mc_sec.try_authentication(data)
                self.user_name = mc_sec.get_user(data)
                if self.authenticated:
                    self.conn.send("Authenticated")
                    self.log(self.user_name + " authenticated.")
                else:
                    self.conn.send("Failed Authentication")
                    self.log(self.user_name + " failed authentication.")
                continue
            if not data: break
            self.server.lock.acquire()
            self.log("Lock acquired for cmd: '" + data + "'")
            result = self.server.run_server_cmd(data)
            self.conn.send(result)
            self.conn.send("MCServer command received correctly.")
            self.server.lock.release()

    def log(self, log_string):
        print self.name + ": " + log_string

def main():
    server = MCServer()
    print "Starting Minecraft server..."
    server.start()
    server.run_server()
    

if __name__ == '__main__':
    main()
