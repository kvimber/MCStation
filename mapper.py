#############################################################
# mapper.py                                                 #
#                                                           #
# by: K.Imber                                               #
#                                                           #
# runs mapping software, and deals with it's input/outputs  #
#############################################################

import shlex, subprocess, time
import properties

class Mapper:

    def __init__(self, server):
        self.server = server

    def run(self):
        print "Running map software..."
        cmd_list = shlex.split(self.server.props[properties.CLI_RUNMAPPER])
        self.p = subprocess.Popen(cmd_list,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        print "Process began."
        while (self.p.returncode is None):
            print "Executing mapping software..."
            time.sleep(2)
            self.p.poll()
        print "Mapping finished.  Exiting."
            
        
