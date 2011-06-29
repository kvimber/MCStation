#############################################
# properties.py                             #
#                                           #
# by: K.Imber                               #
#                                           #
# manages properties for minecart_station   #
#############################################

# these constants define the keys for the dictionary
CLI_RUNSERVER = 'cli.run_server'
CLI_RUNMAPPER = 'cli.run_mapper'
CLI_JVMMEM = 'cli.jvm_mem'
CLI_TIMEOUT = 'cli.timeout'
PATH_SERVER = 'path.server'
PATH_LOGFILE = 'path.log_file'
PATH_MAPFILE = 'path.map_file'
PATH_MAPPER = 'path.mapper'
SMTP_HOST = 'smtp.host'
SMTP_PORT = 'smtp.port'
SMTP_FROMADDR = 'smtp.from_addr'
SMTP_FROMPASS = 'smtp.from_pass'
SMTP_TOADDR = 'smtp.to_addr'
SMTP_TIMEOUT = 'smtp.timeout'
SMTP_SUBJECT = 'smtp.subject'
SMTP_ATTACHFILENAME = 'smtp.attach_filename'
SERVER_PORT = 'server.port'
SERVER_HOST = 'server.host'

# actual property values go below
PROPS = {}
# path to server file, most likely won't change since the server is run
# from the directory by MCServer
PROPS[PATH_SERVER] = "../server"
PROPS[PATH_LOGFILE] = "server.log"
# JVM Memory argument for the minecraft server
PROPS[CLI_JVMMEM] = 1536
# command to run the minecraft server
##CLI_RUNSERVER: "java -Xmx1024M -Xms1024M -jar " + PATH_SERVER + "/minecraft_server.jar nogui",
PROPS[CLI_RUNSERVER] = "java -Xmx" + str(PROPS[CLI_JVMMEM]) + "M -Xms" + str(PROPS[CLI_JVMMEM]) + "M -jar " + PROPS[PATH_SERVER] + "/minecraft_server.jar nogui"
#Timeout for starting the minecraft server
PROPS[CLI_TIMEOUT] = 60
# command to run the map system
PROPS[PATH_MAPPER] = "../mapper"
PROPS[CLI_RUNMAPPER] = PROPS[PATH_MAPPER] + "/mcmap-src/mcmap " + PROPS[PATH_SERVER] + "/world"
# mail server details, default are gmail settings
PROPS[SMTP_HOST] = "smtp.gmail.com"
PROPS[SMTP_PORT] = 465
# server from address login settings
# notice that this shouldn't work with gmail's two factor auth
PROPS[SMTP_FROMADDR] = "kevin.accero@gmail.com"
PROPS[SMTP_FROMPASS] = "baseball!"
# to address for map & notification emails
PROPS[SMTP_TOADDR] = "kvimber@gmail.com"
PROPS[SMTP_TIMEOUT] = 60
# subject of map & notification emails
PROPS[SMTP_SUBJECT] = "Current MC Map"
# path to img file that's output by the map software
PROPS[PATH_MAPFILE] = "output.png"
# filename of the map attachment for emails
PROPS[SMTP_ATTACHFILENAME] = "latest.png"
# server details for MCServer
PROPS[SERVER_PORT] = 9001
PROPS[SERVER_HOST] = "localhost"  
