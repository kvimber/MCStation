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
PATH_LOGFILE = 'path.log_file'
PATH_MAPFILE = 'path.map_file'
SMTP_HOST = 'smtp.host'
SMTP_PORT = 'smtp.port'
SMTP_FROMADDR = 'smtp.from_addr'
SMTP_FROMPASS = 'smtp.from_pass'
SMTP_TOADDR = 'smtp.to_addr'
SMTP_TIMEOUT = 'smtp.time_out'
SMTP_SUBJECT = 'smtp.subject'
SMTP_ATTACHFILENAME = 'smtp.attach_filename'
SERVER_PORT = 'server.port'
SERVER_HOST = 'server.host'

# actual property values go below
PROPS = {
    # command to run the minecraft server
    CLI_RUNSERVER: "java -Xmx1024M -Xms1024M -jar ../server/minecraft_server.jar nogui",
    # command to run the map system
    CLI_RUNMAPPER: "../mcmap-src/mcmap world",
    # path to server file, most likely won't change since the server is run
    # from the directory by MCServer
    PATH_LOGFILE: "server.log",
    # mail server details, default are gmail settings
    SMTP_HOST: "smtp.gmail.com", 
    SMTP_PORT: 465,
    # server from address login settings
    # notice that this shouldn't work with gmail's two factor auth
    SMTP_FROMADDR: "", 
    SMTP_FROMPASS: "",
    # to address for map & notification emails
    SMTP_TOADDR: "", 
    SMTP_TIMEOUT: 30,
    # subject of map & notification emails
    SMTP_SUBJECT: "Current MC Map",
    # path to img file that's output by the map software
    PATH_MAPFILE: "output.png",
    # filename of the map attachment for emails
    SMTP_ATTACHFILENAME: "latest.png",
    # server details for MCServer
    SERVER_PORT: 9001,
    SERVER_HOST: ""
}
        
        
