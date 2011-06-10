#############################################
# props.py                                  #
#                                           #
# by: K.Imber                               #
#                                           #
# manages properties for minecart_station   #
#############################################

# key name constants, so we can just use them across the system
SMTP_HOST = "smtp.host"
SMTP_PORT = "smtp.port"
SMTP_TIMEOUT = "smtp.time_out"
SMTP_FROMADDR = "smtp.from_addr"
SMTP_FROMPASS = "smtp.from_pass"
SMTP_TOADDR = "smtp.to_addr"
SMTP_SUBJECT = "smtp.subject"
SMTP_ATTACHFILENAME = "smtp.attach_filename"

CLI_RUNSERVER = "cli.run_server"
CLI_RUNMAPPER = "cli.run_mapper"

PATH_LOGFILE = "path.log_file"
PATH_MAPFILE = "path.map_file"

IP_PORT = "ip.port"


# properties go here
PROPS = {
    CLI_RUNSERVER: "java -Xmx1024M -Xms1024M -jar minecraft_server.jar nogui",
    CLI_RUNMAPPER: "mcmap-src/mcmap world"
    SMTP_HOST: "smtp.gmail.com",
    SMTP_PORT: "465",
    SMTP_TIMEOUT: 30, 
    SMTP_FROMADDR: "kevin.accero@gmail.com",
    SMTP_FROMPASS: "baseball!",
    SMTP_TOADDR: "kvimber@gmail.com",
    SMTP_SUBJECT: "MC Server Map Notification",
    SMTP_ATTACHFILENAME: "lastmap.png", 
    PATH_LOGFILE: "server.log",
    PATH_MAPFILE: "output.png", 
    IP_PORT: 9001, 
}
