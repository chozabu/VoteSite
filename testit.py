 
import requests

files = {'author': "chozabu", 'name': "ICERUN", "leveldata":"someleveldata", 'sshot':'apicture'}#open('otherthing.txt', 'rb')}
r = requests.post('http://0.0.0.0:8080/uploadLevel', files=files)
print r
print dir(r)
print r.text