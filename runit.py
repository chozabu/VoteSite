from wsgiref.simple_server import make_server
import sys, os
 
# Switch to the virtualenv if we're not already there
#INTERP = os.path.expanduser("~/env/pyramid/bin/python")
 
#if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)
 
from paste.deploy import loadapp
application = loadapp(
    'config:' + 
    os.path.expanduser(os.getcwd()+'/development.ini'))

server = make_server('0.0.0.0', 8080, application)
server.serve_forever()
 
