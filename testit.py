 
import requests

server = 'http://0.0.0.0:8080/'


print ""
print "Create user"
params = {'username': "chozabu", 'password': "asd"}#open('otherthing.txt', 'rb')}
r = requests.post(server+'new_user', data=params)
print r.text

print ""
print "login user"
params = {'username': "chozabu", 'password': "asd"}#open('otherthing.txt', 'rb')}
r = requests.post(server+'login', data=params)
print r.text
session =  r.json()['session']

print ""
print "upload level"
files = {'session':session, 'author': "chozabu", 'name': "ICERUN", "leveldata":"someleveldata", 'sshot':'apicture'}#open('otherthing.txt', 'rb')}
r = requests.post(server+'uploadLevel', files=files)
print r.text


print ""
print "query levels"
params = {'sortKey': "filename", 'cursor': 0, 'limit':8}#open('otherthing.txt', 'rb')}
r = requests.post(server+'query_levels', data=params)
print r.text
#print r
#print dir(r)
