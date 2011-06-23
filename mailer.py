#################################################################
# mailer.py                                                     #
#                                                               #
# by: K.Imber                                                   #
# on: 5.26.11                                                   #
#                                                               #
# this will manage sending mail of any type out from the system #
#################################################################

import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import properties as ps

class Mailer:

    def __init__(self, server):
        self.server = server

    def sendMail(self, mesg):
        try:
            print "Connecting to SMTP Server..."
            server = smtplib.SMTP_SSL(self.server.props[ps.SMTP_HOST], self.server.props[ps.SMTP_PORT], timeout=self.server.props[ps.SMTP_TIMEOUT])
            server.login(self.server.props[ps.SMTP_FROMADDR], self.server.props[ps.SMTP_FROMPASS])
            print "Connection established and user authenticated.  Sending message..."
            server.sendmail(self.server.props[ps.SMTP_FROMADDR], self.server.props[ps.SMTP_TOADDR], mesg)
            print "Message sent.  Closing connection..."
            server.quit()
            print "Connection closed.  Exiting."
        except smtplib.SMTPAuthenticationError:
            print "Server did not accept your username/password combination"
        except smtplib.SMTPSenderRefused:
            print "Server is refusing your sender address.  Please double check this property"
        except smtplib.SMTPServerDisconnected:
            print "The server was disconnected while trying to perform the operation.  Please try again, and if you see this, contact your smtp server admin"
        except smtplib.SMTPConnectError:
            print "There was an error trying to connect to your SMTP Server.  Please double check your properties, and that the server is up and awaiting connections at the correct port"
        except smtplib.SMTPException as exception:
            print "An unforseen error has taken place.  Raising unforseen exception, please send this information to the project maintainers for analysis by our robots..."
            raise exception

    def sendMap(self, to_addr=None):
        print "Generating email..."
        msg = MIMEMultipart()
        msg['Subject'] = self.server.props[ps.SMTP_SUBJECT]
        msg['From'] = self.server.props[ps.SMTP_FROMADDR]
        if to_addr == None:
            msg['To'] = self.server.props[ps.SMTP_TOADDR]
        else:
            msg['To'] = to_addr
##        msg.preamble = 'Preamble for Current MC Map'

        print "  Attaching image to send..."
        img_file = open(self.server.props[ps.PATH_MAPFILE], 'rb')
        img = MIMEImage(img_file.read())
        img_file.close()
        img.add_header('Content-Disposition', 'attachment', filename=self.server.props[ps.SMTP_ATTACHFILENAME])
        msg.attach(img)
        print "Email generated.  Opening SMTP Connection..."

        self.sendMail(msg.as_string())

##        server = smtplib.SMTP_SSL(self.props[SMTP_HOST], self.props[SMTP_PORT], timeout=self.props[TIME_OUT])
##        server.login(self.props[FROM_ADDR], self.props[FROM_PASS])
##        print "Connection established, authentication passed.  Sending message..."
##        server.sendmail(self.props[FROM_ADDR], self.props[TO_ADDR], msg.as_string())
##        print "Message sent.  Closing SMTP Connection..."
##        server.quit()
##        print "Connection closed.  Exiting."
    
    
    
