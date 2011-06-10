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
    CLI_RUNSERVER: "java -Xmx1024M -Xms1024M -jar ../server/minecraft_server.jar nogui", 
    CLI_RUNMAPPER: "../mcmap-src/mcmap world", 
    PATH_LOGFILE: "server.log", 
    SMTP_HOST: "smtp.gmail.com", 
    SMTP_PORT: 465,
    # server from address login settings
    # notice that this won't work with gmail's two factor auth
    SMTP_FROMADDR: "", 
    SMTP_FROMPASS: "", 
    SMTP_TOADDR: "", 
    SMTP_TIMEOUT: 30, 
    SMTP_SUBJECT: "Current MC Map", 
    PATH_MAPFILE: "output.png", 
    SMTP_ATTACHFILENAME: "latest.png", 
    SERVER_PORT: 9001,
    SERVER_HOST: ""
}
        
        
