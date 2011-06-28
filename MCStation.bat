@ECHO OFF
cd server
if (%1)==() GOTO HELP
if (%1)==(server) GOTO SERVER
if (%1)==(adduser) GOTO SECURITY
if (%1)==(client) GOTO CLIENT

:HELP
echo MCStation server..................starts the MCServer and listens for connection
echo MCStation adduser..................sets up a new user for the server
echo MCStation client..................starts the client and attempts a connection
GOTO END

:SERVER
IF NOT EXIST ../core/mc_server.py GOTO NO_SERVER
python ../core/mc_server.py
GOTO END

:SECURITY
python ../core/mc_security.py
GOTO END

:CLIENT
IF NOT EXIST ../core/mc_client.py GOTO NO_CLIENT
python ../core/mc_client.py
GOTO END

:NO_SERVER
echo Error! You appear to not have the MCServer component installed. Please re-run install and select server to install.
GOTO END

:NO_CLIENT
echo Error! You appear to not have the MCClient component installed. Please re-run install and select client to install.
GOTO END


:END